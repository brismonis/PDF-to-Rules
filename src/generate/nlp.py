# In this class we use INDRA to read Statements from text
import os, json, time, threading, requests, re
from pdftorules.settings import MEDIA_ROOT
import concurrent.futures

from indra.assemblers import sif
from indra.sources import reach
from indra.sources import trips
from .models import Files

thread_local = threading.local()


def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session

def nlp_file(f):
    all_statements = []
    PDF_file = Files.get_filename(f)
    JSON_folder = os.path.join(MEDIA_ROOT, 'json') # path to json Folder
    ocrtext = Files.get_ocrtext(f)
    JSON_file = os.path.join(JSON_folder, PDF_file + '_id' + str(f.id) + '_reach.json')
    # with open(JSON_file, 'x') as outfile:
    #     json.dump(txt, outfile)
    start_time = time.time()
    #trips_processor = trips.process_text(ocrtext) 
    reach_processor = reach.process_text(text=ocrtext, output_fname=JSON_file, url=reach.local_text_url)

    # Test: Combining indra-statements -> worked
    # file28 = Files.objects.get(id=33)
    # test_statements = []
    # test_file = os.path.join(JSON_folder, 'igf_id28_reach_test.json')
    # test_processor = reach.process_text(text=file28.ocrtext, output_fname=test_file, url=reach.local_text_url)
    # test_statements = test_processor.statements

    duration = time.time() - start_time
    all_statements = reach_processor.statements

    # Test: Combining indra-statements -> worked
    #combined_statements = all_statements + test_statements
    # print (combined_statements)

    all_evidence = []
    # for ev in all_statements:
    #     evid = '%s with evidence "%s"' % (ev, ev.evidence[0].text)
    #     e = str(evid).replace("\n", " ").replace(" \n", " ").replace("\n ", " ").replace(" \n ", " ")
    #     all_evidence.append(e)

    for ev in all_statements:
        evid = '%s with evidence "%s"' % (ev, ev.evidence[0].text)
        e = str(evid).replace("\n", " ").replace(" \n", " ").replace("\n ", " ").replace(" \n ", " ")
        all_evidence.append(e)

    
    # print("*****************************")
    f.stmlist = all_statements
    f.evidence = all_evidence
    f.evlist = all_evidence
    
    # for a in all_evidence:
    #     f.evidence = f.evidence + a + "\n"
    # #f.evidence = all_evidence
    # print(f.evidence)
    #print("----------------------------")

    # # OLD CODE, calling non local API
    # max_index = 5000
    # index = 0
    # string_length = len(ocrtext)
    # print (string_length)
    # if (string_length <= max_index):
    #     start_time = time.time()
    #     reach_processor = reach.process_text(text=ocrtext, output_fname=JSON_file)#, url=reach.local_text_url)

        
    #     #stm = process_all_text(ocrtext, JSON_file)
    #     #print(stm)
    #     #all_statements.append(stm)
    #     duration = time.time() - start_time
    #     print(f"Processed in {duration} seconds")

    #     all_statements = reach_processor.statements
    #     #print(all_statements)
        
    # else: 
    #     c = 1
    #     while ((index + max_index) <= string_length):
    #         partstr = ocrtext[index:max_index*c]
    #         #print(partstr)
    #         reach_processor = reach.process_text(text=partstr, output_fname=JSON_file)
    #         #, output_fname=JSON_folder)
    #         #stm = reach_processor.statements
    #         all_statements = all_statements + reach_processor.statements
    #         #all_statements + stm
    #         #print(stm)
    #         index = index + max_index
    #         c = c + 1
    #     partstr2 = str(ocrtext[index:string_length])
    #     print(index)
    #     #print (part_str2) #gibt alles aus ??
    #     reach_processor2 = reach.process_text(text=partstr2, output_fname=JSON_file)
    #     #, output_fname=JSON_folder)
    #     #stm2 = reach_processor2.statements
    #     all_statements = all_statements + reach_processor2.statements
    #     #print(all_statements)
    
    #f.stm = all_statements
    #f.save()



# def process_all_text(text, json_dir):
#     with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
#         executor.map(process_reach, text, json_dir)

    
    # for st in reach_processor.statements:
    #     #print('%s with evidence "%s"' % (st, st.evidence[0].text))
    #     print('%s with evidence "%s"' % (st, st.evidence[0].text))
        
        
        # print('%s' % (st))
    
    #return (all_statements)



    #INDRA-Rules umwandeln zu boolschen Funktionen
    BN_folder = os.path.join(MEDIA_ROOT, 'boolean_network') # path to bn Folder
    BN_file = os.path.join(BN_folder, f.filename)

    #test
    # file30 = Files.objects.get(id=30)
    # file29 = Files.objects.get(id=29)
    # stm2930 = file30.stmlist + file29.stmlist

    # file28 = Files.objects.get(id=28)
    # #sa = sif.SifAssembler(stmts=file28.stmlist)
    # readtest = open('igf_id28_sifstring', "r")
    # test = readtest.read()
    # test.mak

    # Test: Combining indra-statements -> worked
    # sa = sif.SifAssembler(stmts=combined_statements)

    #print(all_statements)
    sa = sif.SifAssembler(f.stmlist)
    sa.make_model(use_name_as_key=True, include_mods=True, include_complexes=True)
    #print(sa)
    #sa.make_model(use_name_as_key=True, include_mods=True)
    #sa.make_model(use_name_as_key=True)
    #sa.make_model()
    sa.save_model(fname=BN_file + '_id' + str(f.id) + "_sifstring")
    sa.print_boolean_net(out_file=BN_file + '_id' + str(f.id) +  "_boolnet")
    #bf = ''
    #Zeichen ersetzen, Ausgabe anpassen
    readfile = open(BN_file + '_id' + str(f.id) +  "_boolnet", "r")
    bf = readfile.read()
    x = bf.split("\n\n")
    #print(x[1])

    bool_list = []
    try:
        bool_list = x[1].split("\n")
    except:
        print("No Rules were found for your input!")
        bool_list.append("NO RULES FOUND")
    
    
    rangel = len(bool_list) - 1
    #print(rangel)
    for bf in range(0, rangel):
        nb = bool_list[bf].replace(" not ", " ! ")
        nb = nb.replace("*", "")
        nb = nb.replace(" = ", ", ")
        nb = nb.replace(" or ", " | ")
        nb = nb.replace(" and ", " & ")
        #words = bf.split()
        # removes repeating words by using regex
        nb = re.sub(r'\b(.+)\s+\1\b', r'\1', nb)
        #print(nb)
        #print (len(nb))
        bool_list[bf] = nb
        #print(bf)
        
        #print (" ".join(sorted(set(words), key=words.index)))
        #print(bf)
    
    #print(boolnet)

    # deleting last item in array because it's empty
    del bool_list[-1]
    #print(bool_list)
    readfile.close()
    f.ruleslist = bool_list
    f.rules = bool_list
    f.save()