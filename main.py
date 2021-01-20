import rasterio
import numpy as np
import open3d as o3d
from raster2xyz import Raster2xyz
from geojson_transform import to_geojson
from clipping_tif import zone_defining

dsm = rasterio.open('./Datas/RELIEF_WALLONIE_MNS_2013_2014-002.tif')

zone_to_render = zone_defining(dsm, to_geojson())


def cloudpoint_to_obj(zone):
    """Take the cloud point and save it to a nice .obj object"""
    xyz = Raster2xyz()
    raster = xyz.translate(zone_to_render)
    df = raster[0]
    point_cloud = df.to_numpy()
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(point_cloud)
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(
        radius=0.1, max_nn=30))
    pcd.paint_uniform_color([0.2, 0.8, 0.6])
    distances = pcd.compute_nearest_neighbor_distance()
    avg_dist = np.mean(distances)
    radius = 2.5 * avg_dist
    bpa_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd, o3d.utility.DoubleVector(
        [radius, radius * 2]))
    dec_mesh = bpa_mesh.simplify_quadric_decimation(100000)
    dec_mesh.remove_degenerate_triangles()
    dec_mesh.remove_duplicated_triangles()
    dec_mesh.remove_duplicated_vertices()
    dec_mesh.remove_non_manifold_edges()
    # test to get the coordinates center of the 3d .obj
    # o3d.geometry.get_center(dec_mesh)
    """Saves the cloud point as an .obj object"""
    obj_name = 'test_test' # str(input("Name of the .obj ?: "))
    return o3d.io.write_triangle_mesh("./Datas/" + f"{obj_name}.obj", dec_mesh)
    # return o3d.visualization.draw_geometries([dec_mesh])


if __name__ == "__main__":
    cloudpoint_to_obj(zone_to_render)
