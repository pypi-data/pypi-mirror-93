from typing import Tuple, Union

import numpy as np

import pp
from pp.cell import cell
from pp.component import Component
from pp.components.euler.geo_euler import euler_bend_points, euler_length
from pp.geo_utils import extrude_path
from pp.layers import LAYER
from pp.port import auto_rename_ports


def _bend_euler(
    theta: int = 90,
    radius: Union[int, float] = 10.0,
    width: float = 0.5,
    resolution: float = 150.0,
    layer: Tuple[int, int] = LAYER.WG,
) -> Component:
    c = pp.Component()
    backbone = euler_bend_points(theta, radius=radius, resolution=resolution)
    pts = extrude_path(backbone, width)

    c.add_polygon(pts, layer=layer)
    # print(backbone[0])
    # print(backbone[-1])
    length = euler_length(radius, theta)
    c.info["length"] = length
    c.length = length
    c.radius = radius
    c.add_port(
        name="in0",
        midpoint=np.round(backbone[0].xy, 3),
        orientation=180,
        layer=layer,
        width=width,
    )
    c.add_port(
        name="out0",
        midpoint=np.round(backbone[-1].xy, 3),
        orientation=theta,
        layer=layer,
        width=width,
    )

    return c


@cell
def bend_euler90(
    radius: Union[int, float] = 10.0,
    width: float = 0.5,
    resolution: float = 150.0,
    layer: Tuple[int, int] = LAYER.WG,
) -> Component:
    """
    .. plot::
      :include-source:

      import pp

      c = pp.c.bend_euler90()
      c.plot()

    """
    c = _bend_euler(
        theta=90, radius=radius, width=width, resolution=resolution, layer=layer
    )
    return auto_rename_ports(c)


@cell
def bend_euler90_biased(radius=10.0, width=0.5, resolution=150.0, layer=LAYER.WG):
    width = pp.bias.width(width)
    c = _bend_euler(
        theta=90, radius=radius, width=width, resolution=resolution, layer=layer
    )
    return auto_rename_ports(c)


@cell
def bend_euler180(
    radius: Union[int, float] = 10.0,
    width: float = 0.5,
    resolution: float = 150.0,
    layer: Tuple[int, int] = LAYER.WG,
) -> Component:
    """
    .. plot::
      :include-source:

      import pp

      c = pp.c.bend_euler180()
      c.plot()

    """
    c = _bend_euler(
        theta=180, radius=radius, width=width, resolution=resolution, layer=layer
    )
    return auto_rename_ports(c)


@cell
def bend_euler180_biased(radius=10.0, width=0.5, resolution=150.0, layer=LAYER.WG):
    width = pp.bias.width(width)
    c = _bend_euler(
        theta=180, radius=radius, width=width, resolution=resolution, layer=layer
    )
    return auto_rename_ports(c)


if __name__ == "__main__":
    pass
    c = bend_euler90()
    # c = bend_euler90_biased()
    # c = bend_euler180()
    print(c.ports)
    c.show()
