# bliend_sqli
Bliend SQL Injcetion Attack Python Code
Bliend SQL Injection 공격을 실행하는 코드입니다.

## 사용법
  ```bash
  usage: sqli.py [-h] [-d DATABASE] [-t TABLE [TABLE ...]]
                 [-c COLUMN [COLUMN ...]] -u URL -q QUERY -sign        
                 SIGNATURE [-s STARTER] [-e ENDER] [-ck COOKIE]        
                 [-m METHOD] [-l LIM]
                 execution
  ```

## 옵션
  
1. options:
  ```bash
    -h, --help            show this help message and exit
  ```

2. 필수 옵션:
   반드시 작성해야하는 옵션입니다.
  ```bash  
  -t TABLE [TABLE ...], --table TABLE [TABLE ...]
                        테이블명 지정
  execution             실행할 옵션(db, table, column, data)
  -u URL, --url URL     URL 주소
  -q QUERY, --query QUERY
                        URL 쿼리 파라미터
  -sign SIGNATURE, --signature SIGNATURE
                        True의 시그니처 지정
  ```
  
3. 선택옵션:
  초기값이 있는 옵션들 입니다.

  ```bash
  -d DATABASE, --database DATABASE
                        데이터베이스명 지정. 초기값은 사용중인 DB    
  -c COLUMN [COLUMN ...], --column COLUMN [COLUMN ...]
                        컬럼명 지정
  -s STARTER, --starter STARTER
                        여는 SQL문. 초기값 ' and
  -e ENDER, --ender ENDER
                        닫는 SQL문. 초기값 #
  -ck COOKIE, --cookie COOKIE
                        쿠키값 지정.
  -m METHOD, --method METHOD
                        HTTP 메서드 지정. (G)/P
  -l LIM, --lim LIM     데이터 갯수 제한
  ```
