import io
import unittest
import json
from nmdc.scripts.gff2json import NMDCGFFLoader


class testGFF2JSON(unittest.TestCase):
    def test_GenomeFeature(self):
        """
        Test annotations beyond GenomeFeature.
        """
        gff_str = 'Ga0185794_41\tGeneMark.hmm-2 v1.05\tCDS\t48\t1037\t56.13\t+\t0\tID=Ga0185794_41_48_1037;translation_table=11;start_type=ATG;product=5-methylthioadenosine/S-adenosylhomocysteine deaminase;product_source=KO:K12960;cath_funfam=3.20.20.140;cog=COG0402;ko=KO:K12960;ec_number=EC:3.5.4.28,EC:3.5.4.31;pfam=PF01979;superfamily=51338,51556'
        ai = 'nmdc:4ce9a799923b238585fc952135e5a0f5'
        print(f'Test GenomeFeature ...\n\nInput:\n\t{gff_str}\n')

        with io.StringIO() as fh:
            fh.write(gff_str)
            fh.seek(0)
            parser = NMDCGFFLoader(fh, ai)
            jst = parser.get_json()
            print('Output in JSON:')
            print(jst)
            tmp = json.loads(jst)
            tmp = tmp['Ga0185794_41']['Ga0185794_41_48_1037']
            gf = tmp['genome_feature_set']
            af = tmp['functional_annotation_set']
            self.assertEqual(gf['seqid'], 'nmdc:Ga0185794_41')
            self.assertEqual(gf['start'], 48)
            self.assertEqual(gf['end'], 1037)
            self.assertEqual(gf['strand'], '+')
            self.assertEqual(gf['type'], 'SO:0000316')
            self.assertEqual(af['cog']['has_function'], "EGGNOG:COG0402")
            self.assertEqual(af['ko']['has_function'],
                             "KEGG.ORTHOLOGY:K12960")


if __name__ == '__main__':
    unittest.main()
