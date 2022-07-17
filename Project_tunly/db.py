from fingerprint import fingerprint
import pickle

#Initial database used for correlating the input signal
#Total we have taken 6 wave files of different genre 
# Pop, Rock, Ukulele, funk, oldrock, jazz and dubstep
def init_database():
    database_fp = [0]*6
    database_song = [0]*6
    database_path = [0]*6
    
    database_path[0] = 'database/pop.wav'    
    database_path[1] = 'database/rock.wav'
    database_path[2] = 'database/funk.wav'
    database_path[3] = 'database/dubstep.wav'
    database_path[4] = 'database/ukulele.wav'
    database_path[5] = 'database/jazz.wav'  
    
    database_fp[0] = fingerprint(database_path[0], 0)
    database_fp[1] = fingerprint(database_path[1], 0)
    database_fp[2] = fingerprint(database_path[2], 0)
    database_fp[3] = fingerprint(database_path[3], 0)
    database_fp[4] = fingerprint(database_path[4], 0)
    database_fp[5] = fingerprint(database_path[5], 0)
    
    database_song[0] = 'Pop' 
    database_song[1] = 'Rock'
    database_song[2] = 'Funk'
    database_song[3] = 'Dubstep'
    database_song[4] = 'Ukulele'
    database_song[5] = 'Jazz'
    
    database = [database_song, database_fp, database_path]
        
    with open('database.pickle', 'wb') as f:
            pickle.dump([database], f)
            