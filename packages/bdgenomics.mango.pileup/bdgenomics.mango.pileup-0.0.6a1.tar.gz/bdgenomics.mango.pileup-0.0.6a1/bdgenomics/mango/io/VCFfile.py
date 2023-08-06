#
# Licensed to Big Data Genomics (BDG) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional insourceion
# regarding copyright ownership.  The BDG licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from .genomicfile import GenomicFile
from collections import OrderedDict
import gzip
from bdgenomics.mango.pileup.sources import GA4GHVariantJson

class VCFFile(GenomicFile):

    global VCF_HEADER
    global NUM_SAMPLES
    VCF_HEADER = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT']


    @classmethod
    def _read(cls, filename):
        """Open an optionally gzipped VCF file and return a modin DataFrame with
        each INFO field included as a column in the dataframe.
        
        Borrowed from https://gist.github.com/slowkow/6215557

        Specification: https://samtools.github.io/hts-specs/VCFv4.2.pdf
        :param filename:    An optionally gzipped VCF file.
       
        """
        # Count how many comment lines should be skipped.
        NUM_COMMENTS = cls._count_comments(filename)
        # Return a simple DataFrame without splitting the INFO column.
        df = cls.dataframe_lib.read_table(filename, skiprows=range(NUM_COMMENTS-1))
        NUM_SAMPLES = len(df.columns) - len(VCF_HEADER)
        df.columns = VCF_HEADER + list(range(1, NUM_SAMPLES+1))
        return df       

    @classmethod
    def _getcallinformation(cls, row):
        sample_column_names = row.index[9:]
        call_information = '"calls":['
        for col in sample_column_names:
            current_call = '{'
            call_set_name = '"callSetName":"{}",'.format(str(col))
            info = str(row[col])
            genotype = '"genotype":["{}","{}"],'.format(info[0], info[2])
            phaseset = '"phaseset":"True"'
            current_call = current_call + call_set_name + genotype + phaseset + '},'
            call_information = call_information + current_call
        call_information = call_information[:-1] + ']'
        return call_information
    
    
    @classmethod
    def _parse(cls, df):
        def _buildrow(row):
            reference_name = row["CHROM"]
            start = row["POS"]
            end = start + 1
            reference_bases = row["REF"]
            alternate_bases = row["ALT"]
            ids = row["ID"]
            call_information = cls._getcallinformation(row)
            content = '"referenceName":"{}", "start":"{}", "end":"{}", "referenceBases":"{}", "alternateBases":"{}", "id":"{}", {}'.format(str(reference_name), str(start), str(end), str(reference_bases), str(alternate_bases), str(ids), call_information)
            return content
        return df.apply(_buildrow, axis = 1).squeeze()

    @classmethod
    def _to_json(cls, df):
        content_series = cls._parse(df)
        json_ga4gh = "{\"variants\":["
        json_ga4gh += "{" + content_series.str.cat(sep="},{")[:-2]
        json_ga4gh =  json_ga4gh + "}]}]}"
        
        return json_ga4gh
        
    
    @classmethod
    def _visualization(cls, df):
        return GA4GHVariantJson.name

    @classmethod
    def _count_comments(cls, filename):
        """Count comment lines (those that start with "#") in an optionally
        gzipped file.
        :param filename:  An optionally gzipped file.
        """
        comments = 0
        is_gzip = False

        if filename.endswith('.gz'):
            fn_open = gzip.open
            is_gzip = True
        else:
            fn_open = open

        with fn_open(filename) as fh:
            if is_gzip:
                while True:
                    line = fh.readline().decode("utf-8")
                    if line.startswith("#"):
                        comments += 1
                    else:
                        break
            else:
                for line in fh:
                    if line.startswith('#'):
                        comments += 1
                    else:
                        break
        return comments
