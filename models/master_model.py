def createResponse(result, fields, flag):
    # 1 -> for fetch all data 0 -> for fetch one data
    if flag > 0:
        res_dt = []
        for dt in result:
            resObj = {}
            for i in range(len(fields)):
                resObj[fields[i]] = dt[i]
            res_dt.append(resObj)
    else:    
        resObj = {}
        for i in range(len(fields)):
            resObj[fields[i]] = result[i]
        res_dt = resObj
    return res_dt