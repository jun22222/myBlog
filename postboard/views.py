import os
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, render_to_response
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from postboard.models import DjangoBoard
from django.core.paginator import Paginator
from postboard.models import DjangoBoard

# 업로드=======================================================================================================================

# def upload1(request):
#     if request.method == 'GET':
#         pass
#     else:
#
#         upload_file = request.FILES['file']
#         #
#         try:
#             os.mkdir('upload1')
#         except FileExistsError as e:
#             pass
#         file_name = upload_file.name
#         with open(file_name, 'wb') as file:
#             for chunk in upload_file.chunks():
#                 file.write(chunk)
#         res = {'Ans': '업로드 되었습니다.'}
#         return JsonResponse(res)
# #================================================================================================================================

# def upload2(request):
#     if request.method == 'GET':
#         form = forms.UploadForm
#         return render(request, 'postboard/writeBoard.html', {'form':form})
#     else:
#         form = forms.UploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             try:
#                 os.mkdir('upload2')
#             except FileExistsError as e:
#                 pass
#             upload_file = request.FILES['my_file']
#             file_name = upload_file.name
#             with open('upload2/' + file_name, 'wb') as file:
#                 for chunk in upload_file.chunks():
#                     file.write(chunk)
#         return


# 리스트 뿌려주는ㄴ거
# 게시판 첫페이지=============================================================================================================
# 페이지내이션 기능
def daily(request):
    page = request.GET.get('page')
    if not page:
        page = '1'

    lists = DjangoBoard.objects.order_by('-id')    # 데이터 베이스의 자료들을 내을차순으로 정렬

    paginator = Paginator(lists, 10)     # 정렬된 자료를 10개의 덩어리로 자름
    page_info = paginator.page(page)       # 10개의 덩어리중 괄호안의 페이지에 대한 정보
    #페이지 계산식===========================================
    start_page = (int(page) - 1) // 10 * 10 + 1
    end_page = start_page + 10
    # 마지막 페이지 수에 맞게 범위 재지정====================
    if end_page >= page_info.paginator.num_pages:
       end_page = page_info.paginator.num_pages + 1
    # 마지막 페이지 수에 맞게 범위 재지정====================
    page_range = range(start_page, end_page)
    # 페이지 계산식===========================================
    return render(
        request, 'postboard/daily.html',
        {'lists': page_info, 'page_range': page_range}
    )
# 게시판 첫페이지=============================================================================================================


# 글 조회=============================================================================================================
def viewwork(request, id): # GET 방식으로 입력박을 시 넘어오는 id. urls.py 에서도 path에 입력해줘야함.
    board = DjangoBoard.objects.get(id=id)     # id에 해당하는 정보들
    board.hits = board.hits + 1    # 조회수 증가
    board.save()
                                                        # id 에 해당하는 정보들을 html에 넘겨줘서 사용
                                                        # viewwork.html 에서 {{ board.memo }} 로 내용물 확인 가능
    return render(request, 'postboard/viewwork.html', {'board': board})
# 글 조회=============================================================================================================



# 글 삭제=============================================================================================================
# 게시글에 파일이 첨부되어 있다면 해당 데이터를 조회해서 해당 파일을 삭제 한 후에 게시글을 삭제해줘야한다.
def delBoard(request):
    id = request.POST['id']    # 클릭한 게시글의 아이디를 받아와서
    board = DjangoBoard.objects.get(id=id) # 그 아이디에 맞는 데이터를 DjangoBoard에서 가져옴
    try:
        os.unlink(board.place + board.file)
        # os.unlink('경로와 주소') : 파일 삭제
    except: # 파일이 없을경우 에러가 나고 이쪽으로 온다)
       pass # 삭제할 파일이 없을경우 패스
    board.delete()
    res = {'Ans': '삭제되었습니다.'}
    return JsonResponse(res)
# 글 삭제=============================================================================================================

# 게시판 메인 화면=============================================================================================================
def main(request):
    return render(request, 'postboard/index.html', {})
# 게시판 메인 화면=============================================================================================================


# 글 수정=============================================================================================================
def updateBoard(request, id):         # GET 방식으로 입력박을 시 넘어오는 id. urls.py 에서도 path에 입력해줘야함.
    if request.method == 'GET':
        board = DjangoBoard.objects.get(id=id)
        return render(request,
                      'postboard/updateBoard.html',
                      {'board': board})
    else:   # 수정 페이지에서 넘어오는 것들
        # 첨부파일 첨부 안하고 수정====================================================================================
        try:
            upload_file = request.FILES['my_file']
        except MultiValueDictKeyError:
            DjangoBoard.objects.filter(id=id).update(
                subject=request.POST['subject'],
                mail=request.POST['email'],
                memo=request.POST['memo'],
            )
            url = '/postboard/daily/'
            return HttpResponseRedirect(url)
        # 첨부파일 첨부 안하고 수정====================================================================================
        try:
            os.mkdir('upload1')
        except FileExistsError as e:
            pass
        file_name = upload_file.name
        with open('upload1/' + file_name, 'wb') as file:
            for chunk in upload_file.chunks():
                file.write(chunk)

        DjangoBoard.objects.filter(id=id).update(       # 데이터 수정시에는 해당 데이터에 접근(filter(id=id) 후 업데이트(.update)
            subject=request.POST['subject'],
            mail=request.POST['email'],
            memo=request.POST['memo'],
            file=file_name,
            place='upload1/',
        )

        url = '/postboard/daily/'
        return HttpResponseRedirect(url)
# 글 수정=============================================================================================================
# 글쓰기=============================================================================================================
def writeBoard(request):
    if request.method == 'GET':
        return render(request, 'postboard/writeBoard.html', {})
    else: # submit으로 제출
        # 첨부파일 첨부 안하고 작성====================================================================================
        try:
            upload_files = request.FILES.getlist('my_file')  # submit에 첨부됨 파일
        except MultiValueDictKeyError:
            br = DjangoBoard(subject=request.POST['subject'],
                             name=request.POST['name'],
                             mail=request.POST['email'],
                             memo=request.POST['memo'],
                             created_date=timezone.now(),
                             hits=0,
                             )
            br.save()
            url = '/postboard/daily/'
            return HttpResponseRedirect(url)  # 해당 url로 돌아가기
        # 첨부파일 첨부 안하고 작성====================================================================================
        # 첨부파일 첨부하고 작성시====================================================================================
        try:
            os.mkdir('upload1')
        except FileExistsError as e:
            pass

        for upload_file in upload_files:    # 다중 파일 업로드
            file_name = upload_file.name
            with open('upload1/' + file_name, 'wb') as file:   # 저장경로
                for chunk in upload_file.chunks():
                    file.write(chunk)

            br = DjangoBoard(subject=request.POST['subject'],
                             name=request.POST['name'],
                             mail=request.POST['email'],
                             memo=request.POST['memo'],
                             created_date=timezone.now(),
                             hits=0,
                             file=file_name,
                             place='upload1/',

                             )
            br.save()

        url = '/postboard/daily/'
        return HttpResponseRedirect(url)
        # 첨부파일 첨부하고 작성시====================================================================================
# 글쓰기 =============================================================================================================





# 데이터베이스 추가 ===================================================================================================
def insert(request):
    for i in range(1, 101):  # 게시물 1000개 입력
        br=DjangoBoard(subject='제목' + str(i),
                       name='이름' + str(i),
                       mail='메일' + str(i),
                       memo='내용' + str(i),
                       created_date=timezone.now(),
                       hits=0,
                         )
        br.save()


    return HttpResponse('insert 1000')
# 데이터베이스 추가 ===================================================================================================


