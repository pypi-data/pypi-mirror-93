import o3seespy as o3  # for testing only
import pytest


def test_quad():
    osi = o3.OpenSeesInstance(ndm=2, ndf=2)
    obj = o3.nd_material.ElasticIsotropic(osi, 1, 0.45)
    coords = [[0, 0], [1, 0], [1, 1], [0, 1]]
    ele_nodes = [o3.node.Node(osi, *coords[x]) for x in range(4)]
    o3.element.Quad(osi, ele_nodes=ele_nodes, thick=1.0, otype='PlaneStrain', mat=obj, pressure=1.0, rho=1.0, b1=0.0, b2=0.0)



def test_shell_mitc4():
    osi = o3.OpenSeesInstance(ndm=2)
    coords = [[0, 0], [1, 0], [1, 1], [0, 1]]
    ele_nodes = [o3.node.Node(osi, *coords[x]) for x in range(len(coords))]
    sec = o3.section.Elastic2D(osi, 10.0, 1.0, 1.0)
    o3.element.ShellMITC4(osi, ele_nodes=ele_nodes, sec=sec)


def test_shell_dkgq():
    osi = o3.OpenSeesInstance(ndm=2)
    coords = [[0, 0], [1, 0], [1, 1], [0, 1]]
    ele_nodes = [o3.node.Node(osi, *coords[x]) for x in range(len(coords))]
    sec = o3.section.Elastic2D(osi, 10.0, 1.0, 1.0)
    o3.element.ShellDKGQ(osi, ele_nodes=ele_nodes, sec=sec)


@pytest.mark.skip()  # this is been fixed by needs latest openseespy
def test_shell_dkgt():
    osi = o3.OpenSeesInstance(ndm=2)
    coords = [[0, 0], [1, 0], [1, 1]]
    ele_nodes = [o3.node.Node(osi, *coords[x]) for x in range(len(coords))]
    sec = o3.section.Elastic2D(osi, 10.0, 1.0, 1.0)
    o3.element.ShellDKGT(osi, ele_nodes=ele_nodes, sec=sec)


def test_shell_nldkgq():
    osi = o3.OpenSeesInstance(ndm=2)
    coords = [[0, 0], [1, 0], [1, 1], [0, 1]]
    ele_nodes = [o3.node.Node(osi, *coords[x]) for x in range(len(coords))]
    sec = o3.section.Elastic2D(osi, 10.0, 1.0, 1.0)
    o3.element.ShellNLDKGQ(osi, ele_nodes=ele_nodes, sec=sec)


@pytest.mark.skip()
def test_shell_nldkgt():
    osi = o3.OpenSeesInstance(ndm=2)
    coords = [[0, 0], [1, 0], [1, 1]]
    ele_nodes = [o3.node.Node(osi, *coords[x]) for x in range(len(coords))]
    sec = o3.section.Elastic2D(osi, 10.0, 1.0, 1.0)
    o3.element.ShellNLDKGT(osi, ele_nodes=ele_nodes, sec=sec)


def test_shell_nl():
    osi = o3.OpenSeesInstance(ndm=2)
    coords = [[0, 0], [1, 0], [1, 1], [0, 1], [0.5, 0], [1, 0.5], [0.5, 1], [0, 0.5], [0.5, 0.5]]
    ele_nodes = [o3.node.Node(osi, *coords[x]) for x in range(len(coords))]
    sec = o3.section.Elastic2D(osi, 10.0, 1.0, 1.0)
    o3.element.ShellNL(osi, ele_nodes=ele_nodes, sec=sec)


def test_bbar_quad():
    osi = o3.OpenSeesInstance(ndm=2, ndf=2)
    mat = o3.nd_material.ElasticIsotropic(osi, 1, 0.45)
    coords = [[0, 0], [1, 0], [1, 1], [0, 1]]
    ele_nodes = [o3.node.Node(osi, *coords[x]) for x in range(4)]
    o3.element.BbarQuad(osi, ele_nodes=ele_nodes, thick=1.0, mat=mat)


def test_enhanced_quad():
    osi = o3.OpenSeesInstance(ndm=2, ndf=2)
    obj = o3.nd_material.ElasticIsotropic(osi, 1, 0.45)
    coords = [[0, 0], [1, 0], [1, 1], [0, 1]]
    ele_nodes = [o3.node.Node(osi, *coords[x]) for x in range(4)]
    o3.element.EnhancedQuad(osi, ele_nodes=ele_nodes, thick=1.0, otype='PlaneStress', mat=obj)


def test_ss_pquad():
    osi = o3.OpenSeesInstance(ndm=2)
    obj = o3.nd_material.ElasticIsotropic(osi, 1, 0.45)
    coords = [[0, 0], [1, 0], [1, 1], [0, 1]]
    ele_nodes = [o3.node.Node(osi, *coords[x]) for x in range(4)]
    o3.element.SSPquad(osi, ele_nodes=ele_nodes, mat=obj, otype='PlaneStrain', thick=1.0, b1=0.0, b2=0.0)


if __name__ == '__main__':
    test_bbar_quad()

