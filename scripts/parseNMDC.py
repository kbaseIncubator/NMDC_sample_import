import json
import pandas as pd


def map_to_kbase_tsv(nmdc_db, nmdc_to_kbase__map):
    print("len(nmdc_db[\"biosample_set\"])) " + str(len(nmdc_db["biosample_set"])))
    for sample in nmdc_db["biosample_set"]:
        #print(json.dumps(sample, indent=2))
        #print("\n\n")

        outf = open(outdir + sample["id"].replace(":", "_") + "__KBASEMAP.tsv", "w")

        header = ""
        outstr = ""
        for field in sample:
            print("field " + field)

            mapcol = nmdc_to_kbase__map.loc[:, nmdc_to_kbase__map.columns.str.contains(field)]
            print(mapcol)
            print(type(mapcol))
            print(mapcol.iloc[0][1])
            #exit(0)


            print(sample[field])
            print(type(sample[field]))
            if not type(sample[field]) == str:
                print(len(sample[field]))
                # if len(sample[field]) == 2:
                for field2 in sample[field]:
                    print("field2 " + field2)
                    print(sample[field][field2])
                    #if len(sample[field]) == 1:
                    mapcol = nmdc_to_kbase__map.loc[:, nmdc_to_kbase__map.columns.str.contains(field2)]
                    header = header + mapcol.iloc[0][1] + "\t"
                    #else:
                    #header = header + field + "_" + field2 + "\t"

                    outstr = outstr + str(sample[field][field2]) + "\t"
                    # else if field = "lat_lon":
                    #    for field2 in sample[field]:
                    #        print(field2)
                    #        print(sample[field][field2])
                    #        header = header + field2+"\t"
                    #        outstr = outstr + sample[field][field2]+"\t"
            else:
                header = header + mapcol.iloc[0][1] + "\t"
                outstr = outstr + sample[field] + "\t"



        outf.write(header + "\n")
        outf.write(outstr + "\n")

        outf.close()

def flatten_to_tsv(nmdc_db):
    print("len(nmdc_db[\"biosample_set\"])) " + str(len(nmdc_db["biosample_set"])))
    for sample in nmdc_db["biosample_set"]:
        print(json.dumps(sample, indent=2))
        print("\n\n")

        outf = open(outdir + sample["id"].replace(":", "_") + ".tsv", "w")

        header = ""
        outstr = ""
        for field in sample:
            print("field " + field)
            print(sample[field])
            print(type(sample[field]))
            if not type(sample[field]) == str:
                print(len(sample[field]))
                # if len(sample[field]) == 2:
                for field2 in sample[field]:
                    print("field2 " + field2)
                    print(sample[field][field2])
                    if len(sample[field]) == 1:
                        header = header + field + "\t"
                    else:
                        header = header + field + "_" + field2 + "\t"

                    outstr = outstr + str(sample[field][field2]) + "\t"
                    # else if field = "lat_lon":
                    #    for field2 in sample[field]:
                    #        print(field2)
                    #        print(sample[field][field2])
                    #        header = header + field2+"\t"
                    #        outstr = outstr + sample[field][field2]+"\t"
            else:
                header = header + field + "\t"
                outstr = outstr + sample[field] + "\t"



        outf.write(header + "\n")
        outf.write(outstr + "\n")

        outf.close()
        #break







outdir = "./samples/"

file = open("nmdc_database.json")

line = file.read()
file.close()

nmdc_db = json.loads(line)

# print(json.dumps(nmdc_db, indent=2))

keys_1 = nmdc_db.keys()
# [u'biosample_set', u'data_object_set', u'omics_processing_set', u'study_set', u'activity_set']
print(keys_1)

# print(json.dumps(nmdc_db["biosample_set"], indent=2))

nmdc_to_kbase__map = pd.read_csv("NMDC_KBase_field_mapping.txt", sep='\t')

print(nmdc_to_kbase__map)

map_to_kbase_tsv(nmdc_db, nmdc_to_kbase__map)
#flatten_to_tsv(nmdc_db)




