integrated!
 
import os
import numpy as np

def ioanalysis(transaction_table,X,final_demand,M,phase='',loop='',year='',outputPath=''):
    ''''
    expects numpy arrays: T with extents, (xt, xt)
    that is the same as vectors for Final Demand, Y (xt,1) and
    Primary inputs, V (1, xt) and also one dimenion of a table of
    direct material inputs, M (m, xt). X is assumed to be a row
    vector (1, xt)
    
    All inputs must be fully enumerated (no NaN or text)

    If a non-empty outputs path is specified, results are 
    exported as CSV files, otherwise numpy tables are returned.

    '''
    
    xt = X.shape[1]

    I = np.identity(xt)  
    technical_coefficient = transaction_table/X
    L = np.linalg.inv(I-technical_coefficient)  
    
    direct_intensity_multiplier = M/X
    total_intensity_multiplier = np.transpose(np.dot(direct_intensity_multiplier,L))

    #? name ? Need it for anything?
    FP = total_intensity_multiplier * final_demand
    
    return technical_coefficient,direct_intensity_multiplier,total_intensity_multiplier

    # # checks
    # # print ("M shape", M.shape)
    # # print ("L shape", L.shape)

    # if outputPath == '':
    #     return A, DIM, TIM
    # else:
    #     RESULTSPATH = os.path.join(outputPath,str(phase),str(loop),str(year)) + os.sep
    #     try: 
    #         os.makedirs(RESULTSPATH)
    #     except:
    #         print(RESULTSPATH, " Already exists") 

    #     #np.savetxt(RESULTSPATH +'A.csv',A, delimiter=",")
    #     #check3 = np.matmul(TIM,Y)
    #     #np.savetxt(RESULTSPATH +'Y.csv',Y, delimiter=",")  
    #     np.savetxt(RESULTSPATH +'M.csv',M, delimiter=",")
    #     np.savetxt(RESULTSPATH +'X.csv',X, delimiter=",")
    #     #np.savetxt(RESULTSPATH +'L.csv',L, delimiter=",")
    #     np.savetxt(RESULTSPATH +'TIMs.csv',TIM, delimiter=",")
    #     np.savetxt(RESULTSPATH +'DIMs.csv',DIM, delimiter=",")
    #     np.savetxt(RESULTSPATH +'FP.csv',FP, delimiter=",")

    print ("End of IO Analysis")
    print ("")