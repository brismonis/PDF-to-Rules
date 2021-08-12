# In this class we use INDRA to read Statements from text
import os, json, time, threading, requests
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
    # TODO: getting Object 
    all_statements = []
    PDF_file = Files.get_filename(f)
    JSON_folder = os.path.join(MEDIA_ROOT, 'json') # path to json Folder
    ocrtext = Files.get_ocrtext(f)
    JSON_file = os.path.join(JSON_folder, PDF_file + '_reach.json')
    # with open(JSON_file, 'x') as outfile:
    #     json.dump(txt, outfile)
    start_time = time.time()
    #trips_processor = trips.process_text(ocrtext) 
    reach_processor = reach.process_text(text=ocrtext, output_fname=JSON_file, url=reach.local_text_url)
    duration = time.time() - start_time
    #print(duration)
    #all_statements = trips_processor.statements
    all_statements = reach_processor.statements
    all_evidence = []
    for ev in all_statements:
        #print('%s with evidence "%s"' % (ev, ev.evidence[0].text))
        all_evidence.append(ev.evidence[0].text)

    f.stm = all_statements
    f.evidence = all_evidence

    # # OLD
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

# def process_reach(text, json_dir):
#     print("**************************")
#     stm = []
#     session = get_session()
#     rp = reach.process_text(text=text, output_fname=json_dir)
#     stm = rp.statements
#     return stm



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
    sa = sif.SifAssembler(stmts=all_statements)
    sa.make_model(use_name_as_key=True, include_mods=True, include_complexes=False)
    #sa.save_model(fname=BN_file + "_sifstring")
    sa.print_boolean_net(out_file=BN_file + "_boolnet")
    #bf = ''
    #Zeichen ersetzen, Ausgabe anpassen
    readfile = open(BN_file + "_boolnet", "r")
    bf = readfile.read()
    x = bf.split("\n\n")
    print(x[1])
    boolnet = x[1].replace(" not ", " ¬ ")
    boonet = boolnet.replace("*", "")
    boolnet = boolnet.replace(" or ", " v ")
    boolnet = boolnet.replace(" and ", " ∧ ")
    
    #print(boolnet)


    readfile.close()
    f.rules = boolnet
    f.save



    #sa.print_loopy(BN_file + "_loopy")
    
    #sifstring = sa.print_model
    #sa2 = sif.SifAssembler(all_statements).save_model(fname=BN_file + ".txt")
    #print(sa2)
    #str = sa.print_boolean_net(out_file=BN_file)
    #sa.make_model
    #print(sifstring)


    #TODO: Boolsche Funktionen als csv speichern + download