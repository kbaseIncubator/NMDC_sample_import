import json


def file_dict(fn, globalkey):
    with open(fn) as f:
        data = json.loads(f.read())
    data = data[globalkey]
    kv = dict()
    for p in data:
        id = p['id']
        kv[id] = dict()
        kv[id]['id'] = id
        kv[id]['name'] = p['name']
        kv[id]['description'] = p.get('description')
        if 'part_of' in p:
            kv[id]['part_of'] = p['part_of'][0]
        for a in p['annotations']:
           k=a["has_characteristic"]['name']
           v=a["has_raw_value"]
           kv[id][k] = v
    return kv
study_prefix = 'study_'
omics_prefix = 'omics_process_'

#nmdc_db["biosample_set"]
omics_proc = file_dict('/Users/marcin/Documents/KBase/kbaseapps/NMDC_sample_import/nmdc_database.json', 'omics_processing_set')
samples = file_dict('/Users/marcin/Documents/KBase/kbaseapps/NMDC_sample_import/nmdc_database.json', 'biosample_set')
studies = file_dict('/Users/marcin/Documents/KBase/kbaseapps/NMDC_sample_import/nmdc_database.json', 'study_set')


s_fields = [
          "name",
          "descriptoin",
          "ecosystem",
          "ecosystem_category",
          "ecosystem_type",
          "ecosystem_subtype",
          "specific_ecosystem",
          "ecosystem_path_id",
          "principal_investigator_name",
          "doi"
          ]
o_fields = ["instrument_name", "ncbi_project_name", "omics_type", "principal_investigator_name", "processing_institution" ]
b_fields = [
	'id',
        'name',
        'description',
        'add_date',
        'mod_date',
        'sample_collection_site',
        'sample_collection_day',
        'sample_collection_month',
        'sample_collection_year',
        'ncbi_taxonomy_name',
        'geographic_location',
        'location',
        'latitude',
        'longitude',
        'identifier',
        'depth',
        'habitat',
        'community',
        'ecosystem',
        'ecosystem_path_id',
        'ecosystem_category',
        'ecosystem_type',
        'ecosystem_subtype',
        'specific_ecosystem'
        ]
fields = b_fields
fields.extend(map(lambda x: omics_prefix+x, o_fields))
fields.extend(map(lambda x: study_prefix+x, s_fields))
print('\t'.join(fields))
for sample in sorted(samples.keys()):
   kv = samples[sample]
   ordered = []
   pid = kv['part_of']
   for f in o_fields:
       kv[omics_prefix+f] = omics_proc[pid].get(f, '')
   sid = omics_proc[pid]['part_of']
   for f in s_fields:
       kv[study_prefix+f] = studies[sid].get(f, '')
   for k in fields:
       ordered.append(str(kv.get(k, '')))
   print('\t'.join(ordered))
