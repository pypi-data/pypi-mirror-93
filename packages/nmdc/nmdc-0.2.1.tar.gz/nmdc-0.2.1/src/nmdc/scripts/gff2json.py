"""
Methods to convert NMDC GFF3 to JSON
"""
import os
import json
import re

import obonet
from BCBio import GFF
from nmdc.metadata import schema


class NMDCGenomeFeature(schema.GenomeFeature):
    """
    NMDC GenomeFeature with JSON export functionality
    """
    def __init__(self, ai, seqid, start, end, **kargs):
        super().__init__(seqid, start, end, **kargs)
        assert(isinstance(kargs, dict))
        genome_feature = {'seqid': seqid,
                          'start': start,
                          'end': end}
        for k in kargs:
            genome_feature.update({k: kargs[k]})
        self.properties = {'genome_feature_set': genome_feature,
                           'functional_annotation_set': {}}
        self._ACCEPTABLE_KEYS = ['cog',
                                 'product',
                                 'smart',
                                 'cath_funfam',
                                 'ko',
                                 'ec_number',
                                 'pfam',
                                 'superfamily'
                                 ]
        self.ai = ai            # activity index

    def __repr__(self):
        repr = f'NMDCGenomeFeature seqid: {self.seqid}.'
        return repr

    def __dict__(self):
        return self.properties

    def get_json(self, indent=2):
        """
        Get JSON dump.
        """
        js = json.dump(self.__dict__(), indent=indent)
        return js

# From nmdc-metadata scripts/gff3_converter.py
    @staticmethod
    def prepare_curie(k: str, term: str) -> str:
        """

    ￼    Given a key and a term, prepare a CURIE for the term.
    ￼
    ￼    Parameters
    ￼    ----------
    ￼    k: str
    ￼        The key
    ￼    term: str
    ￼        A database entity
    ￼
    ￼    Returns
    ￼    -------
    ￼    str
    ￼        A CURIE representation of the given term
    ￼
    ￼    """
        if re.match(r"^[^ <()>:]*:[^/ :]+$", term):
            prefix, reference = term.split(':', 1)
            if prefix == 'KO':
                curie = f"KEGG.ORTHOLOGY:{reference}"
            else:
                curie = term
        else:
            if k.lower() == 'ko':
                curie = f"KEGG.ORTHOLOGY:{term}"
            elif k.lower() == 'pfam':
                curie = f"PFAM:{term}"
            elif k.lower() == 'smart':
                curie = f"SMART:{term}"
            elif k.lower() == 'cog':
                curie = f"EGGNOG:{term}"
            elif k.lower() == 'cath_funfam':
                curie = f"CATH:{term}"
            elif k.lower() == 'superfamily':
                curie = f"SUPFAM:{term}"
            elif k.lower() == 'product':
                curie = term
            else:
                curie = f":{term}"
        return curie

    def add_annotation(self, adict, feature_id):
        """
        Add annotation dictionary to GenomeFeature
        """
        for (k, v) in adict.items():
            k = k.lower()
            if k in self._ACCEPTABLE_KEYS:
                assert(isinstance(v, list))
                for t in v:
                    term_curie = NMDCGenomeFeature.prepare_curie(k, t)
                    functional_annotation = {
                        'subject': f"nmdc:{feature_id}",
                        'has_function': term_curie,
                        'was_generated_by': self.ai,
                        #'type': "NMDC:FunctionalAnnotation"
                    }
                    if k not in self.properties['functional_annotation_set'].keys():
                        self.properties['functional_annotation_set'].update(
                            {k: functional_annotation})
                    else:
                        pass


class NMDCGFFLoader:
    """
    Load a GFF a file and map its contents to NMDC GenomeFeature
    """
    # TODO: Better use a generator to generate json per line of gff
    def __init__(self, gfffh, ai):
        """
        Load a NMDC GFF3 file and convert it to JSON.

        gfffh: GFF file handler ready to read.
        ai: activity index string
        """
        SOOBO = os.path.join(os.path.dirname(schema.__file__),
                             'so-simple.obo')
        sograph = obonet.read_obo(SOOBO)
        sddict = {data.get('name'): id_
                  for id_, data in sograph.nodes(data=True)}

        jd = {}

        for rec in GFF.parse(gfffh):
            rd = {}
            for feature in rec.features:
                feature_id = feature.id
                feature_type = feature.type
                if feature_type in sddict.keys():
                    feature_type_so = sddict[feature_type]
                else:
                    feature_type_so = None
                feature_start = int(feature.location.start)
                feature_end = int(feature.location.end)
                feature_strand = feature.location.strand
                if feature_strand == 1:  # 1 for '+' strand
                    feature_strand = '+'
                elif feature_strand == -1:  # -1 for '-' strand
                    feature_strand = '-'
                elif feature_strand is None:  # None for '' strand
                    feature_strand = ''
                seqid = f'nmdc:{rec.id}'
                if feature_type_so is None:  # avoid "null" type info.
                    nmdc_gf = NMDCGenomeFeature(
                        ai=ai,
                        seqid=seqid,
                        start=feature_start + 1,  # switch to 1-based counting
                        end=feature_end,
                        strand=feature_strand,
                        encodes=f'nmdc:{feature_id}'
                    )
                else:
                    nmdc_gf = NMDCGenomeFeature(
                        ai=ai,
                        seqid=seqid,
                        start=feature_start + 1,  # switch to 1-based counting
                        end=feature_end,
                        strand=feature_strand,
                        type=feature_type_so,
                        encodes=f'nmdc:{feature_id}'
                    )
                nmdc_gf.add_annotation(feature.qualifiers, feature_id)
                rd.update({feature_id: nmdc_gf.__dict__()})
            jd.update({rec.id: rd})
        self.model = jd

    def get_json(self, indent=2):
        """
        Return data as JSON dump
        """
        return json.dumps(self.model, indent=indent)
