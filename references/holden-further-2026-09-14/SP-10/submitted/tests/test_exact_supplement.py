import unittest,sys
from pathlib import Path
from fractions import Fraction as Q
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from exact_supplement import *
class Checks(unittest.TestCase):
    def test_rank_zero(self): self.assertEqual(rank([[0,0],[0,0]]),0)
    def test_rank_fraction(self): self.assertEqual(rank([[Q(1,2),1],[1,2]]),1)
    def test_rank_identity(self): self.assertEqual(rank([[1,0],[0,1]]),2)
    def test_ragged_rejected(self):
        with self.assertRaises(ValueError): rank([[1],[1,2]])
    def test_bipartite_validation(self):
        with self.assertRaises(ValueError): polynomial_vectors(2,2,[(0,1)])
    def test_degree_validation(self):
        with self.assertRaises(ValueError): polynomial_vectors(2,1,[(0,2),(1,2)],d=1)
    def test_empty_edges(self): self.assertEqual(rank(polynomial_vectors(3,3,[])),1)
    def test_all_edges(self): polynomial_vectors(3,3,[(i,3+j) for i in range(3) for j in range(3)])
    def test_mixed_degrees(self): polynomial_vectors(4,4,[(0,4),(0,5),(2,5),(0,6),(1,6),(2,6),(3,6)],d=4)
    def test_one_empty_part(self): self.assertEqual(rank(polynomial_vectors(0,4,[])),1)
    def test_halfgraph(self):
        k=5; e=[(i,k+j) for i in range(k) for j in range(k) if i<=j]
        self.assertEqual(rank(polynomial_vectors(k,k,e)),k+1)
    def test_sdp_strictness(self):
        f=sdp_fixture(); self.assertEqual(f['a']*f['c']-f['b']**2,Q(25,32))
    def test_sdp_complement(self):
        support(sdp_fixture()['B'],complement(4,[(0,1),(1,2),(2,3)]))
    def test_sdp_missing_edge_rejected(self):
        with self.assertRaisesRegex(ValueError,'support mismatch'): support(sdp_fixture()['X'],[(0,1),(1,2),(2,3)])
    def test_sdp_complementary_slackness(self):
        f=sdp_fixture()
        self.assertTrue(all(sum(f['S'][i][k]*f['X'][k][j] for k in range(4))==0 for i in range(4) for j in range(4)))
    def test_sdp_ranks(self):
        f=sdp_fixture(); self.assertEqual([rank(f[x]) for x in ['C','S','X','B']],[2,2,2,4])
if __name__=='__main__': unittest.main()
