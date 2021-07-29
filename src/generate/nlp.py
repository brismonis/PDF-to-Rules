# In this class we use INDRA to read Statements from text
from indra.sources import reach
from indra.sources import trips
from .models import Files

def nlp_file(f):
    # TODO: getting Object 
    ocrtext = Files.get_ocrtext(f)
    all_statements = []
    part_str = ""
    max_index = 3000
    index = 0
    string_length = len(ocrtext)
    print (string_length)
    if (string_length <= max_index):
        reach_processor = reach.process_text(ocrtext) 
        all_statements = reach_processor.statements
        print(all_statements)
        #bis hier funktionert alles super
    else:
        while ((index + max_index) <= string_length):
            part_str = ocrtext[index:max_index]
            reach_processor = reach.process_text(part_str)
            #stm = reach_processor.statements
            all_statements = all_statements + reach_processor.statements
            #all_statements + stm
            #print(stm)
            index = index + max_index
        part_str2 = ocrtext[index:string_length]
        #print (part_str2) #gibt alles aus ??
        reach_processor2 = reach.process_text(part_str2) 
        #stm2 = reach_processor2.statements
        all_statements = all_statements + reach_processor2.statements
        print(all_statements)
    
    f.rules = all_statements
    f.save()
    
    # for st in reach_processor.statements:
    #     #print('%s with evidence "%s"' % (st, st.evidence[0].text))
    #     print('%s with evidence "%s"' % (st, st.evidence[0].text))
        
        
        # print('%s' % (st))
    
    #return (all_statements)
    #TODO: INDRA-Rules umwandeln zu boolschen Funktionen 


    #TODO: Boolsche Funktionen als csv speichern