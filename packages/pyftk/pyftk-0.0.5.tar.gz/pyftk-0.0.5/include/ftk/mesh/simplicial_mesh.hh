#ifndef _SIMPLICIAL_MESH_HH
#define _SIMPLICIAL_MESH_HH

namespace ftk {

template <typename I>
struct simplicial_mesh {
  simplicial_mesh(int n, const std::vector<I> &conn, const std::vector<float> &vertices);
  simplicial_mesh(std::shared_ptr<simplicial_mesh> base);

  int nd() const; { return simplices.size()-1; }
  int n(I i) const { if (i > 0) return simplices[k].size(); else return vertices.dim(1); }
  bool is_extruded() const { return base_mesh(); }

  std::vector<I> get_simplex(int k, I i) const;
  bool get_simplex(int k, I i, I vert[]) const;
  std::set<I> sides(int k, I i) const;
  std::set<I> sideofs(int k, int i) const;

protected:
  void build_subsimplices(int k);

protected:
  std::shared_ptr<simplicial_mesh> base_mesh;
  std::vector<ndarray<I>> simplices;
  ndarray<float> vertices;
  std::map<std::vector<I>, I> id_map;
  std::map<I, std::set<I>> side_map, sideof_map;
};

//////////////
template <typename I>
simplicial_mesh::simplicial_mesh(int n, const std::vector<I> &conn, const std::vector<float> &coords)
{
  simplices.resize(n+1);

  auto &nsimplices = simplices[n];
  nsimplices.from_vector(conn);
  nsimplices.reshape(n+1, conn.size() / (n+1));
  for (int i = 0; i < nsimplices.dim(1); i ++) { // reorder vertices in each simplex
    std::vector<I> v;
    for (int j = 0; j < n+1; j ++) 
      v[j] = nsimplices(j, i);
    std::sort(v.begin(), v.end());
    for (int j = 0; j < n+1; j ++) 
      nsimplices(j, i) = v[j];
  }

  for (int k = n-1; k >= 0; k --) // build subsimplices
    build_subsimplices(k);
}

template <typename I>
simplicial_mesh::build_subsimplices(int k)
{
  int count = 0;
  for (auto i = 0; i < n(k+1); i ++) {
    const auto simplex = get_simplex(k+1, i);
    for (int j = 0; j < k+1; j ++) {
      if (k == 0) {

      } else {
        std::vector<I> subsimplex;
        for (int j1 = 0; j1 < k+1; j ++)
          if (j != j1)
            subsimplex.push_back(simplex[j1]);

        I id;
        if (id_map.find(subsimplex) != id_map.end()) {
          id = count ++;
          id_map[subsimplex] = id;
        } else 
          id = id_map[subsimplex];

        side_map[i].insert(id);
        sideof_map[id].insert(i);
      }
    }
  }
}

}

#endif
