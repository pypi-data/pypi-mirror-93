""" HMesh is a halfedge based mesh library. It is one of the 
"""
import ctypes as ct
import numpy as np
from numpy.linalg import norm
from pygel3d import lib_py_gel, IntVector, Vec3dVector


class Manifold:
    """ The Manifold class represents a halfedge based mesh.
    Generally, meshes based on the halfedge representation must be manifold. Hence,
    the name. This class contains methods for mesh manipulation and inspection.
    """
    def __init__(self,orig=None):
        if orig == None:
            self.obj = lib_py_gel.Manifold_new()
        else:
            self.obj = lib_py_gel.Manifold_copy(orig.obj)
    @classmethod
    def from_triangles(cls,vertices, faces):
        m = cls()
        m.obj = lib_py_gel.Manifold_from_triangles(len(vertices),len(faces),np.array(vertices,dtype=np.float64), np.array(faces,dtype=ct.c_int))
        return m
    @classmethod
    def from_points(cls,pts,xaxis=np.array([1,0,0]),yaxis=np.array([0,1,0])):
        m = cls()
        m.obj = lib_py_gel.Manifold_from_points(len(pts),np.array(pts,dtype=np.float64), np.array(xaxis,dtype=np.float64), np.array(yaxis,dtype=np.float64))
        return m
    def __del__(self):
        lib_py_gel.Manifold_delete(self.obj)
    def add_face(self,pts):
        """ Add a face to the Manifold.
        This function takes a list of points as argument and creates a face
        in the mesh with those points as vertices.
        """
        lib_py_gel.Manifold_add_face(self.obj, len(pts), np.array(pts))
    def positions(self):
        """ Retrieve an array containing vertex positions. """
        pos = ct.POINTER(ct.c_double)()
        n = lib_py_gel.Manifold_positions(self.obj, ct.byref(pos))
        return np.ctypeslib.as_array(pos,(n,3))
    def no_allocated_vertices(self):
        """ Number of vertices.
        This number could be higher than the number of actually
        used vertices, but corresponds to the number of slots
        allocated."""
        return lib_py_gel.Manifold_no_allocated_vertices(self.obj)
    def no_allocated_faces(self):
        """ Number of faces.
        This number could be higher than the number of actually
        used faces, but corresponds to the number of slots
        allocated."""
        return lib_py_gel.Manifold_no_allocated_faces(self.obj)
    def no_allocated_halfedges(self):
        """ Number of halfedges.
        This number could be higher than the number of actually
        used halfedges, but corresponds to the number of slots
        allocated."""
        return lib_py_gel.Manifold_no_allocated_halfedges(self.obj)
    def vertices(self):
        """ Returns an iterable containing all vertex indices"""
        verts = IntVector()
        n = lib_py_gel.Manifold_vertices(self.obj, verts.obj)
        return verts
    def faces(self):
        """ Returns an iterable containing all face indices"""
        faces = IntVector()
        n = lib_py_gel.Manifold_faces(self.obj, faces.obj)
        return faces
    def halfedges(self):
        """ Returns an iterable containing all halfedge indices"""
        hedges = IntVector()
        n = lib_py_gel.Manifold_halfedges(self.obj, hedges.obj)
        return hedges
    def circulate_vertex(self,v,mode='v'):
        """ Circulate a vertex. Passed a vertex index, v, and second argument,
        mode='f', this function will return an iterable with all faces incident
        on v arranged in counter clockwise order. Similarly, if mode is 'h',
        incident halfedges (outgoing) are returned, and for mode = 'v', all
        neighboring vertices are returned. """
        nbrs = IntVector()
        n = lib_py_gel.Manifold_circulate_vertex(self.obj, v, ct.c_char(mode.encode('ascii')), nbrs.obj)
        return nbrs
    def circulate_face(self,f,mode='v'):
        """ Circulate a face. Passed a face index, f, and second argument,
        mode='f', this function will return an iterable with all faces that
        share an edge with f (in counter clockwise order). If the argument is
        mode='h', the halfedges themselves are returned. For mode='v', the
        incident vertices of the face are returned. """
        nbrs = IntVector()
        n = lib_py_gel.Manifold_circulate_face(self.obj, f, ct.c_char(mode.encode('ascii')), nbrs.obj)
        return nbrs
    def next_halfedge(self,hid):
        """ Returns next halfedge to the one passed as argument. """
        return lib_py_gel.Walker_next_halfedge(self.obj, hid)
    def prev_halfedge(self,hid):
        """ Returns previous halfedge to the one passed as argument. """
        return lib_py_gel.Walker_prev_halfedge(self.obj, hid)
    def opposite_halfedge(self,hid):
        """ Returns opposite halfedge to the one passed as argument. """
        return lib_py_gel.Walker_opposite_halfedge(self.obj, hid)
    def incident_face(self,hid):
        """ Returns face corresponding to halfedge passed as argument. """
        return lib_py_gel.Walker_incident_face(self.obj, hid)
    def incident_vertex(self,hid):
        """ Returns vertex corresponding to halfedge passed as argument. """
        return lib_py_gel.Walker_incident_vertex(self.obj, hid)
    def remove_vertex(self,vid):
        """ Remove a vertex from the Manifold. This function merges all faces
        around the vertex into one and then removes this resulting face. """
        return lib_py_gel.Manifold_remove_vertex(self.obj, vid)
    def remove_face(self,fid):
        """ Removes a face from the Manifold. If it is an interior face it is
        simply replaced by an invalid index. If the face contains boundary
        edges, these are removed. Situations may arise where the mesh is no
        longer manifold because the situation at a boundary vertex is not
        homeomorphic to a half disk. This, we can probably ignore since from the
        data structure point of view it is not really a problem that a vertex is
        incident on two holes - a hole can be seen as a special type of face.
        The function returns false if the index of the face is not valid,
        otherwise the function must complete. """
        return lib_py_gel.Manifold_remove_face(self.obj, fid)
    def remove_edge(self,hid):
        """ Remove an edge from the Manifold. This function will remove the
        faces on either side and the edge itself in the process. Thus, it is a
        simple application of remove_face. """
        return lib_py_gel.Manifold_remove_edge(self.obj, hid)
    def vertex_in_use(self,vid):
        """ check if vertex is in use. This function returns true if the id corresponds
        to a vertex that is currently in the mesh and false otherwise. The id could
        be outside the range of used ids and it could also correspond to a vertex
        which is not active. The function returns false in both cases. """
        return lib_py_gel.Manifold_vertex_in_use(self.obj, vid)
    def face_in_use(self,fid):
        """ check if face is in use. This function returns true if the id corresponds
        to a face that is currently in the mesh and false otherwise. The id could
        be outside the range of used ids and it could also correspond to a face
        which is not active. The function returns false in both cases. """
        return lib_py_gel.Manifold_face_in_use(self.obj, fid)
    def halfedge_in_use(self,hid):
        """ check if halfedge is in use. This function returns true if the id corresponds
        to a halfedge that is currently in the mesh and false otherwise. The id could
        be outside the range of used ids and it could also correspond to a halfedge
        which is not active. The function returns false in both cases. """
        return lib_py_gel.Manifold_halfedge_in_use(self.obj, hid)
    def flip_edge(self,hid):
        """ Flip the edge separating two faces. The function first verifies that
        the edge is flippable. This entails making sure that all of the
        following are true.
        1.  adjacent faces are triangles.
        2. neither end point has valency three or less.
        3. the vertices that will be connected are not already.
        If the tests are passed, the flip is performed and the function
        returns True. Otherwise False."""
        return lib_py_gel.Manifold_flip_edge(self.obj,hid)
    def collapse_edge(self,hid, avg_vertices=False):
        """ Collapse an edge.
        Before collapsing, a number of tests are made:
        ---
        1.  For the two vertices adjacent to the edge, we generate a list of all their neighbouring vertices.
        We then generate a  list of the vertices that occur in both these lists.
        That is, we find all vertices connected by edges to both endpoints of the edge and store these in a list.
        2.  For both faces incident on the edge, check whether they are triangular.
        If this is the case, the face will be removed, and it is ok that the the third vertex is connected to both endpoints.
        Thus the third vertex in such a face is removed from the list generated in 1.
        3.  If the list is now empty, all is well.
        Otherwise, there would be a vertex in the new mesh with two edges connecting it to the same vertex. Return false.
        4.  TETRAHEDRON TEST:
        If the valency of both vertices is three, and the incident faces are triangles, we also disallow the operation.
        Reason: A vertex valency of two and two triangles incident on the adjacent vertices makes the construction collapse.
        5.  VALENCY 4 TEST:
        If a triangle is adjacent to the edge being collapsed, it disappears.
        This means the valency of the remaining edge vertex is decreased by one.
        A valency two vertex reduced to a valency one vertex is considered illegal.
        6.  PREVENT MERGING HOLES:
        Collapsing an edge with boundary endpoints and valid faces results in the creation where two holes meet.
        A non manifold situation. We could relax this...
        7. New test: if the same face is in the one-ring of both vertices but not adjacent to the common edge,
        then the result of a collapse would be a one ring where the same face occurs twice. This is disallowed as the resulting
        face would be non-simple.
        If the tests are passed, the collapse is performed and the function
        returns True. Otherwise False."""
        return lib_py_gel.Manifold_collapse_edge(self.obj, hid, avg_vertices)
    def split_face_by_edge(self,fid,v0,v1):
        """   Split a face. The face, f, is split by creating an edge with
        endpoints v0 and v1 (the next two arguments). The vertices of the old
        face between v0 and v1 (in counter clockwise order) continue to belong
        to f. The vertices between v1 and v0 belong to the new face. A handle to
        the new face is returned. """
        return lib_py_gel.Manifold_split_face_by_edge(self.obj, fid, v0, v1)
    def split_face_by_vertex(self,fid):
        """   Split a polygon, f, by inserting a vertex at the barycenter. This
        function is less likely to create flipped triangles than the
        split_face_triangulate function. On the other hand, it introduces more
        vertices and probably makes the triangles more acute. A handle to the
        inserted vertex is returned. """
        return lib_py_gel.Manifold_split_face_by_vertex(self.obj,fid)
    def split_edge(self,hid):
        """   Insert a new vertex on halfedge h. The new halfedge is insterted
        as the previous edge to h. A handle to the inserted vertex is returned. """
        return lib_py_gel.Manifold_split_edge(self.obj,hid)
    def stitch_boundary_edges(self,h0,h1):
        """   Stitch two halfedges. Two boundary halfedges can be stitched
        together. This can be used to build a complex mesh from a bunch of
        simple faces. """
        return lib_py_gel.Manifold_stitch_boundary_edges(self.obj, h0, h1)
    def merge_faces(self,hid):
        """   Merges two faces into a single polygon. The first face is f. The
        second face is adjacent to f along the halfedge h. This function returns
        true if the merging was possible and false otherwise. Currently merge
        only fails if the mesh is already illegal. Thus it should, in fact,
        never fail. """
        if self.is_halfedge_at_boundary(hid):
            return False
        fid = self.incident_face(hid)
        return lib_py_gel.Manifold_merge_faces(self.obj, fid, hid)
    def close_hole(self,hid):
        """ Close hole given by hid (i.e. the face referenced by hid). Returns
        index of the created face or the face that was already there if, in
        fact, hid was not next to a hole. """
        return lib_py_gel.Manifold_close_hole(self.obj, hid)
    def cleanup(self):
        """ Remove unused items from Mesh, map argument is to be used for
        attribute vector cleanups in order to maintain sync."""
        lib_py_gel.Manifold_cleanup(self.obj)
    def is_halfedge_at_boundary(self, hid):
        """ Returns True if halfedge is a boundary halfedge, i.e. face on either
        side is invalid. """
        return lib_py_gel.is_halfedge_at_boundary(self.obj, hid)
    def is_vertex_at_boundary(self, vid):
        """ Returns True if vertex lies at a boundary. """
        return lib_py_gel.is_vertex_at_boundary(self.obj, vid)
    def edge_length(self, hid):
        """ Returns length of edge passed as argument. """
        return lib_py_gel.length(self.obj, hid)
    # def boundary_edge(self,vid):
    #     hid = 0
    #     if not lib_py_gel.boundary_edge(self.obj,vid,hid):
    #         return None
    #     return hid
    def valency(self,vid):
        """ Returns valency, i.e. number of incident edges."""
        return lib_py_gel.valency(self.obj,vid)
    def vertex_normal(self, vid):
        """ Returns vertex normal (angle weighted) """
        n = (ct.c_double*3)()
        lib_py_gel.vertex_normal(self.obj, vid, ct.byref(n))
        return np.array([n[0],n[1],n[2]])
    def connected(self, v0, v1):
        """ Returns true if the two argument vertices are in each other's one-rings."""
        return lib_py_gel.connected(self.obj,v0,v1)
    def no_edges(self, fid):
        """ Compute the number of edges of a face """
        return lib_py_gel.no_edges(self.obj, fid)
    def face_normal(self, fid):
        """ Compute the normal of a face. If the face is not a triangle,
        the normal is not defined, but computed using the first three
        vertices of the face. """
        n = (ct.c_double*3)()
        lib_py_gel.face_normal(self.obj, fid, ct.byref(n))
        return np.array([n[0],n[1],n[2]])
    def area(self, fid):
        """ Returns the area of a face. """
        return lib_py_gel.area(self.obj, fid)
    def perimeter(self, fid):
        """ Returns the perimeter of a face. """
        return lib_py_gel.perimeter(self.obj, fid)
    def centre(self, fid):
        """ Returns the centre of a face. """
        v = (ct.c_double*3)()
        lib_py_gel.centre(self.obj, fid, ct.byref(v))
        return v

def valid(m):
    """  Verify Manifold Integrity Performs a series of tests to check that this
    is a valid manifold. This function is not rigorously constructed but seems
    to catch all problems so far. The function returns true if the mesh is valid
    and false otherwise. """
    return lib_py_gel.valid(m.obj)

def closed(m):
    """ Returns true if the mesh is closed, i.e. has no boundary."""
    return lib_py_gel.closed(m.obj)

def bbox(m):
    """ Returns the min and max corners of the bounding box of the manifold. """
    pmin = (ct.c_double*3)()
    pmax = (ct.c_double*3)()
    lib_py_gel.bbox(m.obj, ct.byref(pmin),ct.byref(pmax))
    return (np.ctypeslib.as_array(pmin,3),np.ctypeslib.as_array(pmax,3))

def bsphere(m):
    """ Calculate the bounding sphere of the manifold.
    Returns centre,radius """
    c = (ct.c_double*3)()
    r = (ct.c_double)()
    lib_py_gel.bsphere(m.obj,ct.byref(c),ct.byref(r))
    return (c,r)

def stitch(m, rad=1e-30):
    """ Stitch together edges whose endpoints coincide geometrically. This
    function allows you to create a mesh as a bunch of faces and then stitch
    these together to form a coherent whole. What this function adds is a
    spatial data structure to find out which vertices coincide. The return value
    is the number of edges that could not be stitched. Often this is because it
    would introduce a non-manifold situation."""
    return lib_py_gel.stitch_mesh(m.obj,rad)

def obj_save(fn, m):
    """ Save Manifold to Wavefront obj file. """
    s = ct.c_char_p(fn.encode('utf-8'))
    lib_py_gel.obj_save(s, m.obj)

def off_save(fn, m):
    """ Save Manifold to OFF file. """
    s = ct.c_char_p(fn.encode('utf-8'))
    lib_py_gel.off_save(s, m.obj)

def x3d_save(fn, m):
    """ Save Manifold to X3D file. """
    s = ct.c_char_p(fn.encode('utf-8'))
    lib_py_gel.x3d_save(s, m.obj)

def obj_load(fn):
    """ Load Manifold from Wavefront obj file. """
    m = Manifold()
    s = ct.c_char_p(fn.encode('utf-8'))
    if lib_py_gel.obj_load(s, m.obj):
        return m
    return None

def off_load(fn):
    """ Load Manifold from OFF file. """
    m = Manifold()
    s = ct.c_char_p(fn.encode('utf-8'))
    if lib_py_gel.off_load(s, m.obj):
        return m
    return None

def ply_load(fn):
    """ Load Manifold from Stanford PLY file. """
    m = Manifold()
    s = ct.c_char_p(fn.encode('utf-8'))
    if lib_py_gel.ply_load(s, m.obj):
        return m
    return None

def x3d_load(fn):
    """ Load Manifold from X3D file. """
    m = Manifold()
    s = ct.c_char_p(fn.encode('utf-8'))
    if lib_py_gel.x3d_load(s, m.obj):
        return m
    return None

from os.path import splitext
def load(fn):
    """ Load a Manifold from an X3D/OBJ/OFF/PLY file. """
    name, extension = splitext(fn)
    if extension.lower() == ".x3d":
        return x3d_load(fn)
    if extension.lower() == ".obj":
        return obj_load(fn)
    if extension.lower() == ".off":
        return off_load(fn)
    if extension.lower() == ".ply":
        return ply_load(fn)
    return None

def save(fn, m):
    """ Save a Manifold to an X3D/OBJ/OFF file. """
    name, extension = splitext(fn)
    if extension.lower() == ".x3d":
        x3d_save(fn, m)
    elif extension.lower() == ".obj":
        obj_save(fn, m)
    elif extension.lower() == ".off":
        off_save(fn, m)


def remove_caps(m, thresh=2.9):
    """ Remove caps from a manifold consisting of only triangles. A cap is a
    triangle with two very small angles and an angle close to pi, however a cap
    does not necessarily have a very short edge. Set the ang_thresh to a value
    close to pi. The closer to pi the _less_ sensitive the cap removal. A cap is
    removed by flipping the (long) edge E opposite to the vertex V with the
    angle close to pi. However, the function is more complex. Read code and
    document more carefully !!! """
    lib_py_gel.remove_caps(m.obj,thresh)

def remove_needles(m, thresh=0.05, average_positions=False):
    """  Remove needles from a manifold consisting of only triangles. A needle
    is a triangle with a single very short edge. It is moved by collapsing the
    short edge. The thresh parameter sets the length threshold."""
    abs_thresh = thresh * average_edge_length(m)
    lib_py_gel.remove_needles(m.obj,abs_thresh, average_positions)

def close_holes(m, max_size=100):
    """  This function replaces holes by faces. It is really a simple function
    that just finds all loops of edges next to missing faces. """
    lib_py_gel.close_holes(m.obj, max_size)

def flip_orientation(m):
    """  Flip the orientation of a mesh. After calling this function, normals
    will point the other way and clockwise becomes counter clockwise """
    lib_py_gel.flip_orientation(m.obj)

def merge_coincident_boundary_vertices(m, rad = 1.0e-30):
    """  Merg vertices that are boundary vertices and coincident.
        However, if one belongs to the other's one ring or the onr
        rings share a vertex, they will not be merged. """
    lib_py_gel.merge_coincident_boundary_vertices(m.obj, rad)

def minimize_curvature(m,anneal=False):
    """ Minimizes mean curvature. This is really the same as dihedral angle
    minimization, except that we weight by edge length. """
    lib_py_gel.minimize_curvature(m.obj, anneal)

def minimize_dihedral_angle(m,max_iter=10000, anneal=False, alpha=False, gamma=4.0):
    """ Minimizes dihedral angles.
        Arguments:
        max_iter is the maximum number of iterations for simulated annealing.
        anneal tells us the code whether to apply simulated annealing
        alpha=False means that we use the cosine of angles rather than true angles (faster)
        gamma is the power to which the angles are raised."""
    lib_py_gel.minimize_dihedral_angle(m.obj, max_iter, anneal,alpha,ct.c_double(gamma))


def maximize_min_angle(m,dihedral_thresh=0.95,anneal=False):
    """ Maximizes the minimum angle of triangles. Makes the mesh more Delaunay."""
    lib_py_gel.maximize_min_angle(m.obj,dihedral_thresh,anneal)

def optimize_valency(m,anneal=False):
    """ Tries to achieve valence 6 internally and 4 along edges. """
    lib_py_gel.optimize_valency(m.obj, anneal)

def randomize_mesh(m,max_iter=1):
    """  Make random flips. Useful for generating synthetic test cases. """
    lib_py_gel.randomize_mesh(m.obj, max_iter)

def quadric_simplify(m,keep_fraction,singular_thresh=1e-4,optimal_positions=True):
    """ Garland Heckbert simplification in our own implementation. keep_fraction
    is the fraction of vertices to retain. The singular_thresh defines how small
    singular values from the SVD we accept. It is relative to the greatest
    singular value. If optimal_positions is true, we reposition vertices.
    Otherwise the vertices are a subset of the old vertices."""
    lib_py_gel.quadric_simplify(m.obj, keep_fraction, singular_thresh,optimal_positions)

def average_edge_length(m,max_iter=1):
    """ Returns the average edge length. """
    return lib_py_gel.average_edge_length(m.obj)

def median_edge_length(m,max_iter=1):
    """ Returns the median edge length """
    return lib_py_gel.median_edge_length(m.obj)

def refine_edges(m,threshold):
    """ Split all edges in mesh passed as first argument which are longer
    than the threshold (second arg) length. A split edge
    results in a new vertex of valence two."""
    return lib_py_gel.refine_edges(m.obj, threshold)

def cc_split(m):
    """ Perform a Catmull-Clark split, i.e. a split where each face is divided
    into new quadrilateral faces formed by connecting a corner with a point on
    each incident edge and a point at the centre of the face."""
    lib_py_gel.cc_split(m.obj)

def loop_split(m):
    """ Perform a loop split where each edge is divided into two segments, and
    four new triangles are created for each original triangle. """
    lib_py_gel.loop_split(m.obj)

def root3_subdivide(m):
    """ Leif Kobbelt's subdivision scheme, where a vertex is positions in the
    center of each face and all old edges are flipped. """
    lib_py_gel.root3_subdivide(m.obj)

def rootCC_subdivide(m):
    """ This subd. scheme creates a vertex inside each original (quad) face,
    producing four triangles. Triangles sharing an old edge are then merged.
    Two steps produce something similar to Catmull-Clark. """
    lib_py_gel.rootCC_subdivide(m.obj)

def butterfly_subdivide(m):
    """ An interpolatory scheme. Creates the same connectivity as Loop. """
    lib_py_gel.butterfly_subdivide(m.obj)

def cc_smooth(m):
    """ If called after cc_split, this function completes a Catmull-Clark
    subdivision step. """
    lib_py_gel.cc_smooth(m.obj)

def loop_smooth(m):
    """ If called after Loop split, this function completes a step of Loop
    subdivision. """
    lib_py_gel.loop_smooth(m.obj)

def triangulate(m, clip_ear=True):
    """ Turn a general polygonal mesh into a triangle mesh by repeatedly
        splitting a polygon into smaller polygons. """
    if clip_ear:
        lib_py_gel.ear_clip_triangulate(m.obj)
    else:
        lib_py_gel.shortest_edge_triangulate(m.obj)


class MeshDistance:
    """ This class allows you to compute the distance from any point in space to
    a Manifold. The constructor creates an instance based on a specific mesh,
    and the signed_distance function computes the actual distance. """
    def __init__(self,m):
        self.obj = lib_py_gel.MeshDistance_new(m.obj)
    def __del__(self):
        lib_py_gel.MeshDistance_delete(self.obj)
    def signed_distance(self,pts,upper=1e30):
        """ Compute the signed distance from p to the mesh stored in this class
        instance. The distance is positive if outside and negative inside. The
        upper parameter can be used to threshold how far away the distance is of
        interest. """
        p = np.reshape(np.array(pts,dtype=ct.c_float), (-1,3))
        n = p.shape[0]
        d = np.ndarray(n, dtype=ct.c_float)
        p_ct = p.ctypes.data_as(ct.POINTER(ct.c_float))
        d_ct = d.ctypes.data_as(ct.POINTER(ct.c_float))
        lib_py_gel.MeshDistance_signed_distance(self.obj,n,p_ct,d_ct,upper)
        return d
    def ray_inside_test(self,pts,no_rays=3):
        """Check whether a point is inside or outside the stored by casting rays.
        Effectively, this is the sign of the distance. In some cases casting (multiple)
        ray is more robust than using the sign computed locally. """
        p = np.reshape(np.array(pts,dtype=ct.c_float), (-1,3))
        n = p.shape[0]
        s = np.ndarray(n, dtype=ct.c_int)
        p_ct = p.ctypes.data_as(ct.POINTER(ct.c_float))
        s_ct = s.ctypes.data_as(ct.POINTER(ct.c_int))
        lib_py_gel.MeshDistance_ray_inside_test(self.obj,n,p_ct,s_ct,no_rays)
        return s

