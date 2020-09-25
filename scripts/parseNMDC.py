import json
import pandas as pd
import numpy as np

def map_to_kbase_tsv(nmdc_db, nmdc_to_kbase__map):

###
### STUDY IDS
###
    sample_to_study = dict()
    studies = []
    print("len(nmdc_db[\"study_set\"])) " + str(len(nmdc_db["study_set"])))
    countno = 0
    for omics in nmdc_db["omics_processing_set"]:
        # print("OMICS")
        # print(omics)
        try:
            sample_to_study[omics["has_input"][0]] = omics["part_of"][0]
            studies.append(omics["part_of"][0])
        except:
            countno = countno + 1
            # print("no has_input or part_of")

    print("countno " + str(countno))

    studies = list(set(studies))

###
### STUDY DATA
###
    study_data_list = []
    columns = []
    for study in nmdc_db["study_set"]:
        print("STUDY")
        print(json.dumps(study, indent=2))
        print("\n\n")

        header_add = ""
        outstr_add = ""
        count = 0

        row_data = {}
        row = {}

        # only for studies with linked biosamples
        proceed = False
        for field in study:
            if (field == "id"):
                if (study[field] in studies):
                    proceed = True
                    print("proceed")
                    break
        if (proceed):
            for field in study:
                print("field " + field)
                print(study[field])
                print(type(study[field]))

                if type(study[field]) == dict:

                    if 'has_raw_value' in study[field]:
                        header_add = header_add + field + "\t"
                        row_data[field] = str(study[field]['has_raw_value'])
                        # row_data.append(str(study[field]['has_raw_value']))
                        if (count == 0):
                            columns.append(field)
                else:
                    header_add = header_add + field + "\t"
                    row_data[field] = str(study[field])
                    # row_data.append(str(study[field]))
                    if (count == 0):
                        columns.append(field)

            if (count == 0):
                count = 1

        print(header_add)
        print("row_data")
        print(row_data)
        # study_data.append()
        # row[study['id']] = row_data

        study_data_list.append(row_data)

    print(len(study_data_list))
    study_data_df = pd.DataFrame(study_data_list)

    print("study_data_df")
    print(study_data_df.shape)
    print(study_data_df.describe())
    print(study_data_df)

    study_data_df.to_csv("study_data_df.tsv", sep="\t")


###
### SAMPLE DATA
###
    print("len(nmdc_db[\"biosample_set\"])) " + str(len(nmdc_db["biosample_set"])))
    for sample in nmdc_db["biosample_set"]:
        #print(json.dumps(sample, indent=2))
        #print("\n\n")
        #print(sample["id"])

        ###
        ###
        #if(sample["id"] == "gold:Gb0093306"):
            ###
            ###

        outf = open(outdir + sample["id"].replace(":", "_") + "__KBASEMAP.tsv", "w")

        header = ""
        outstr = ""

        study_id = None
        for i in range(len(nmdc_to_kbase__map.columns)):

            col = nmdc_to_kbase__map.columns[i]
            print("col "+col)
            done = 0
            col_clean = col
            if(".1" in col):
                col_clean  = col.replace(".1","")

            print("col "+col)
            for field in sample:
                #print("col_clean " + col_clean+"\t"+field)
                if(col_clean == field):

                    print("field " + field)
                    searchstr = "^"+col+"$"
                    #print(searchstr)
                    mapcol = nmdc_to_kbase__map.filter(regex=searchstr)#nmdc_to_kbase__map.columns.str.findall("^"+field+"$")
                    #mapcol = nmdc_to_kbase__map[index]#nmdc_to_kbase__map.loc[:, index]

                    print("mapcol "+mapcol)
                    #print(mapcol.iloc[1])

                    if (not mapcol.empty):
                        print(mapcol.columns)
                        maphit = list(mapcol.columns)[0]
                        print("maphit "+maphit)
                        mapcolfield = mapcol.iloc[0][0]

                        #print("mapcolfield "+mapcolfield)
                        #print(mapcol.iloc[1])
                        #print(sample[field])

                        ###when field value is an array
                        if not type(sample[field]) == str:
                            print("NESTED "+str(len(sample[field])))

                            for field2 in sample[field]:
                                print("field2 " + field2)
                                print(sample[field][field2])

                                ###special case: add two values from field, mapped to different metedata fields
                                ####NOT YET MODELED IN THE TXT MAPPING FILE
                                if(field2 != "id" and field2 != "hss_raw_value"):# and sample[field][field2].find("{") == -1:
                                    #case of duplicate column names in pandas -- when using a field multiple times in mapping
                                    if field == "lat_lon" or field == "lat_lon.1":
                                        print("lat_lon's "+str(field)+"\t"+str(sample[field]))
                                        for field2 in sample[field]:
                                            print("lat_lon field2 "+field2)
                                            print("lat_lon "+mapcol.iloc[1][0])
                                            if(field2 == mapcol.iloc[1][0]):
                                                print("lat_lon field2 "+field2)
                                                print("lat_lon str(sample[field][field2]) "+str(sample[field][field2]))
                                                if(field2 !=  "has_raw_value"):
                                                    print("ADD lat_lon " + mapcolfield + "\t" + str(sample[field][field2]))
                                                    header = header + field2 + "\t"
                                                    outstr = outstr + str(sample[field][field2])+"\t"
                                                    done = 1
                                        #oddly adds multiple here otherwise
                                        break
                                    elif (field == "depth"):
                                        data_split = str(sample[field][field2]).split(" ")
                                        header = header + mapcolfield + "\t"
                                        outstr = outstr + data_split[0] + "\t"
                                        # hard-coded
                                        header = header + "depth_scale" + "\t"
                                        outstr = outstr + data_split[1] + "\t"
                                        print("ADD depth  " + data_split[0])
                                        print("ADD depth_scale " + data_split[1])
                                        done = 1
                                    elif (field == "geo_loc_name"):
                                        header = header + mapcolfield + "\t"
                                        outstr = outstr + str(sample[field][field2]) + "\t"
                                        print("ADD nested geo_loc_name " + mapcolfield + "\t" + str(sample[field][field2]))
                                        done = 1
                                        #TODO split city, state, country but check cases

                                    else:
                                        if(type(sample[field][field2]) is not dict):
                                            header = header + mapcolfield + "\t"
                                            outstr = outstr + str(sample[field][field2]) + "\t"
                                            print("ADD nested " + mapcolfield + "\t" + str(sample[field][field2]))
                                            done = 1
                        else:
                            print("ADD str "+mapcolfield+"\t"+str(sample[field]))
                            header = header + mapcolfield + "\t"
                            outstr = outstr + str(sample[field]) + "\t"
                            if(field == 'id'):
                                study_id = sample_to_study[sample[field]]
                                #print("study_id "+study_id)
                            done = 1

                    ###other fields not being transformed
                    else:
                        pass

            ###catching empty
            if(done == 0):
                header = header + col + "\t"
                outstr = outstr + "" + "\t"
                print("ADD empty " + col)
                if(col == "depth"):
                    header = header + "depth_scale" + "\t"
                    outstr = outstr + "" + "\t"
                    print("ADD empty " + "depth_scale")

        print("study_data_df.columns.values "+str(type(study_data_df.columns.values)))
        header = header + study_data_df.columns.values
        print("study_id " + str(study_id))
        row_index = np.where(study_data_df["id"] == study_id)
        print("row_index "+str(row_index))

        found_row = study_data_df.loc[study_data_df['id'] == study_id]
        print("found_row "+str(found_row.shape))
        print(found_row)
        print(found_row.values)
        print(np.fromstring(found_row.values))
        print(type(found_row.values))
        print(type( np.array2string(found_row.values, precision=2, separator="\t")))
        outstr = outstr + np.array2string(found_row.values, precision=2, separator="\t")

        print(str(header))
        print(outstr)

        outf.write(str(header) + "\n")
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
            else:
                header = header + field + "\t"
                outstr = outstr + sample[field] + "\t"



        outf.write(header + "\n")
        outf.write(outstr + "\n")

        outf.close()




###
###
###


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

nmdc_to_kbase__map = pd.read_csv("NMDC_KBase_field_mapping_v2.txt", sep='\t')

print(nmdc_to_kbase__map)

map_to_kbase_tsv(nmdc_db, nmdc_to_kbase__map)
#flatten_to_tsv(nmdc_db)




