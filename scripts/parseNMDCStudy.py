import json
import pandas as pd

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

#exit(0)

print("len(nmdc_db[\"study_set\"])) " + str(len(nmdc_db["study_set"])))
for study in nmdc_db["study_set"]:
    print(json.dumps(study, indent=2))
    print("\n\n")

    header_add = ""
    outstr_add = ""
    for field in study:
        print("field " + field)
        print(sample[field])
        print(type(sample[field]))
        if not type(sample[field]) == unicode:
            print(len(sample[field]))
            # if len(sample[field]) == 2:
            for field2 in sample[field]:
                print("field2 " + field2)
                print(sample[field][field2])
                if len(sample[field]) == 1:
                    header_add = header_add + field + "\t"
                else:
                    header_add = header_add + field + "_" + field2 + "\t"

                    outstr_add = outstr_add + str(sample[field][field2]) + "\t"
                # else if field = "lat_lon":
                #    for field2 in sample[field]:
                #        print(field2)
                #        print(sample[field][field2])
                #        header = header + field2+"\t"
                #        outstr = outstr + sample[field][field2]+"\t"
        else:
            header_add = header_add + field + "\t"
            outstr_add = outstr_add + sample[field] + "\t"

    #outf = open(outdir + sample["id"].replace(":", "_") + ".tsv", "w")


    print(header_add)
    print(outstr_add)


print("len(nmdc_db[\"biosample_set\"])) " + str(len(nmdc_db["biosample_set"])))

    for sample in nmdc_db["biosample_set"]:
        print(json.dumps(sample, indent=2))
        print("\n\n")

        header = ""
        outstr = ""
        for field in sample:
            print("field " + field)

            mapcol = nmdc_to_kbase__map.loc[:, nmdc_to_kbase__map.columns.str.startswith('alp')]
            print(mapcol)

            exit(0)

            print(sample[field])
            print(type(sample[field]))
            if not type(sample[field]) == unicode:
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



        #outf.write(header + "\n")
        #outf.write(outstr + "\n")

        #outf.close()
        #break

