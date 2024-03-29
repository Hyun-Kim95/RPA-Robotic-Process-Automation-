    #Project) 나도코딩에서 구독자 분들을 대상으로 파이썬 특강을 진행합니다.
    #참여 신청은 이메일을 통해서 가능하며 메일 수신 시간 기준으로 선착순 3명이 선정됩니다.
    #아래 조건에 해당하는 메일을 자동으로 조회하여 선정되신 분들께는 선정 안내 메일을,
    #아쉽게 선정되지 못한 분들께는 대기 번호 안내 메일을 자동으로 발신하고,
    #선정된 3명의 명단을 엑셀 파일로 저장하는 자동화 프로그램을 작성하시오.

    #[신청 메일 양식]
    #제목 : 파이썬 특강 신청합니다.
    #본문 : 닉네임/전화번호 뒤 4자리 (Random)
    #    (예) 나도코딩/1234

    #[선정 안내 메일]
    #제목 : 파이썬 특강 안내 [선정]
    #본문 : xx님 축하드립니다. 특강 대상자로 선정되셨습니다. (선정순번 1번)

    #[탈락 안내 메일]
    #제목 : 파이썬 특강 안내 [탈락]
    #본문 : xx님 아쉽게도 탈락입니다. 취소 인원이 발생하는 경우 연락드리겠습니다. (대기순번 1번)

    #[선정 명단 엘셀]
    #순번 닉네임 전화번호
    #1   유재석   9429
    #2   박명수   2463
    #3   정형돈   9236

    ########### 실제 메일 생겨질 모습 ###########
    #파이썬 특강 안내 [탈락]
    #파이썬 특강 안내 [탈락]
    #파이썬 특강 안내 [선정]
    #파이썬 특강 안내 [선정]
    #파이썬 특강 안내 [선정]
    #파이썬 특강 신청합니다.
    #파이썬 특강 신청합니다.
    #파이썬 특강 신청합니다.
    #파이썬 특강 신청합니다.
    #파이썬 특강 신청합니다.

# 테스트 메일 발신
    import smtplib
    from account import *
    from random import *
    from email.message import EmailMessage

    nicknames = ["유재석", "박명수", "정형돈", "노홍철", "조세호"]

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        for nickname in nicknames:
            msg = EmailMessage()
            msg["subject"] = "파이썬 특강 신청합니다."
            msg["From"] = EMAIL_ADDRESS
            msg["To"] = "khyun9512@gmail.com"

            # content = nickname + "/" + str(randint(1000,9999))    # 둘중 아무거나 써도 됨
            content = "/".join([nickname, str(randint(1000,9999))]) # 둘중 아무거나 써도 됨
            
            msg.set_content(content)
            smtp.send_message(msg)
            print(nickname + "님이 김현 계정으로 메일을 발송 완료")

# 메일 필터링
    from account import *
    from imap_tools import MailBox

    applicant_list = [] # 지원자 리스트

    with MailBox("imap.gmail.com", 993).login(EMAIL_ADDRESS, EMAIL_PASSWORD, initial_folder="INBOX") as mailbox:
        index = 1   # 순번
        for msg in mailbox.fetch('(SENTSINCE 26-Jan-2021)'):    # 2021년 1월 26일 이후로 온 메일 조회
            if "파이썬 특강" in msg.subject:
                nickname, phone = msg.text.strip().split("/")   # strip을 붙혀서 줄바꿈 없앴음
                print("순번 : {} 닉네임 : {} 전화번호 : {}".format(index, nickname, phone))
                applicant_list.append((msg, index, nickname, phone))
                index += 1

# 선정 탈락 여부 메일 발신
    import smtplib
    from account import *
    from imap_tools import MailBox
    from email.message import EmailMessage

    max_val = 3         # 최대 선정자 수
    applicant_list = [] # 지원자 리스트

    print("[1. 지원자 메일 조회]")

    with MailBox("imap.gmail.com", 993).login(EMAIL_ADDRESS, EMAIL_PASSWORD, initial_folder="INBOX") as mailbox:
        index = 1   # 순번
        for msg in mailbox.fetch('(SENTSINCE 26-Jan-2021)'):    # 2021년 1월 26일 이후로 온 메일 조회
            if "파이썬 특강" in msg.subject:
                nickname, phone = msg.text.strip().split("/")   # strip을 붙혀서 줄바꿈 없앴음
                # print("순번 : {} 닉네임 : {} 전화번호 : {}".format(index, nickname, phone))
                applicant_list.append((msg, index, nickname, phone))
                index += 1

    print("[2. 선정 / 탈락 메일 발송]")

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        for applicant in applicant_list:
            to_addr = applicant[0].from_    # 수신 메일 주소
            index, nickname, phone = applicant[1:]

            title = None
            content = None

            if index <= max_val:
                title = "파이썬 특강 안내 [선정]"
                content = "{}님 축하드립니다. 특강 대상자로 선정되셨습니다. (선정순번 {}번)".format(nickname, index)
            else:
                title = "파이썬 특강 안내 [탈락]"
                content = "{}님 아쉽게도 탈락입니다. 취소 인원이 발생하는 경우 연락드리겠습니다. (대기순번 {}번)".format(nickname, index - max_val)

            msg = EmailMessage()
            msg["Subject"] = title
            msg["From"] = EMAIL_ADDRESS
            msg["To"] = to_addr
            msg.set_content(content)
            smtp.send_message(msg)
            print(nickname, "님에게 메일 발송 완료")

# 선정자 명단 엑셀 제작(완성작)
    import smtplib
    from openpyxl import Workbook
    from account import *
    from imap_tools import MailBox
    from email.message import EmailMessage

    max_val = 3 # 최대 선정자 수
    applicant_list = [] # 지원자 리스트

    print("[1. 지원자 메일 조회]")

    with MailBox("imap.gmail.com", 993).login(EMAIL_ADDRESS, EMAIL_PASSWORD, initial_folder="INBOX") as mailbox:
        index = 1   # 순번
        for msg in mailbox.fetch('(SENTSINCE 26-Jan-2021)'):    # 2021년 1월 26일 이후로 온 메일 조회
            if "파이썬 특강 신청합니다." in msg.subject:
                nickname, phone = msg.text.strip().split("/")   # strip을 붙혀서 줄바꿈 없앴음
                # print("순번 : {} 닉네임 : {} 전화번호 : {}".format(index, nickname, phone))
                applicant_list.append((msg, index, nickname, phone))
                index += 1

    print("[2. 선정 / 탈락 메일 발송]")
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        for applicant in applicant_list:
            to_addr = applicant[0].from_    # 수신 메일 주소
            # index = applicant[1]
            # nickname = applicant[2]
            # phone = applicant[3]
            index, nickname, phone = applicant[1:]

            title = None
            content = None

            if index <= max_val:
                title = "파이썬 특강 안내 [선정]"
                content = "{}님 축하드립니다. 특강 대상자로 선정되셨습니다. (선정순번 {}번)".format(nickname, index)
            else:
                title = "파이썬 특강 안내 [탈락]"
                content = "{}님 아쉽게도 탈락입니다. 취소 인원이 발생하는 경우 연락드리겠습니다. (대기순번 {}번)".format(nickname, index - max_val)

            msg = EmailMessage()
            msg["Subject"] = title
            msg["From"] = EMAIL_ADDRESS
            msg["To"] = to_addr
            msg.set_content(content)
            smtp.send_message(msg)
            print(nickname, "님에게 메일 발송 완료")

    print("[3. 선정자 명단 파일 생성]")

    wb = Workbook()
    ws = wb.active
    ws.append(["순번", "닉네임", "전화번호"])

    for applicant in applicant_list[:max_val]:
        ws.append(applicant[1:])

    wb.save("result.xlsx")

    print("모든 작업이 완료되었습니다.")
