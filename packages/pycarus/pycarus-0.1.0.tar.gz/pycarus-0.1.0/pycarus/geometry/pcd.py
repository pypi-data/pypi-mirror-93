from pathlib import Path
from typing import Union

import open3d as o3d  # type: ignore
import torch


def read_pcd(pcd_path: Union[str, Path]) -> torch.Tensor:
    """Read a point cloud from a given file.

    The point cloud is returned as a torch tensor with shape (N, D).
    D can be 3 (only XYZ coordinates), 6 (XYZ coordinates and
    normals) or 9 (XYZ coordinates, normals and colors).

    Args:
        pcd_path: the path of the point cloud file.

    Raises:
        ValueError: if the given file doesn't exist.

    Returns:
        A torch tensor with the loaded point cloud.
    """
    pcd_path = Path(pcd_path)
    if not pcd_path.exists():
        raise ValueError(f"The pcd file {str(pcd_path)} does not exists.")

    pcd_o3d = o3d.io.read_point_cloud(str(pcd_path))
    pcd_torch = torch.tensor(pcd_o3d.points)

    if len(pcd_o3d.normals) > 0:
        normals_torch = torch.tensor(pcd_o3d.normals)
        pcd_torch = torch.cat((pcd_torch, normals_torch), dim=-1)

    if len(pcd_o3d.colors) > 0:
        colors_torch = torch.tensor(pcd_o3d.colors)
        pcd_torch = torch.cat((pcd_torch, colors_torch), dim=-1)

    return pcd_torch
