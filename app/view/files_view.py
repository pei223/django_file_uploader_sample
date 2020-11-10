import logging
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .form.file_form import FileSelectForm, FileUploadForm
import traceback

from ..domain.file_record import RegisterFileRecord
from ..infra.file_record_repository import FileRecordRepository

logger = logging.getLogger("default")

_SAVE_RESPONSE_PARAM = "save_result"
_DOWNLOAD_RESPONSE_PARAM = "download_result"
_DELETE_RESPONSE_PARAM = "delete_result"

_PAGINATE_BY = 2


class FilesView(LoginRequiredMixin, View):
    def get(self, request):
        request.GET.get(_SAVE_RESPONSE_PARAM)
        user_id = request.user.id
        data_count = FileRecordRepository().data_count(user_id)
        paginator = _get_paginator(request, data_count, _PAGINATE_BY)

        file_records = FileRecordRepository().get_user_files(user_id, page_num=paginator.number,
                                                             paginate_by=_PAGINATE_BY)

        form = FileUploadForm()
        context = {
            "paginator": paginator,
            "form": form,
            "file_records": file_records,
        }
        return render(request, "files.html", context)

    def post(self, request):
        user = request.user
        form = FileUploadForm(request.POST, request.FILES)
        if not form.is_valid():
            return _error_response(_SAVE_RESPONSE_PARAM)

        file_ = form.cleaned_data["file"]
        repo = FileRecordRepository()
        repo.register_file_record(user, RegisterFileRecord(file_=file_))
        return redirect(f"/files?{_SAVE_RESPONSE_PARAM}=success")


@login_required
def file_delete_view(request):
    form = FileSelectForm(request.GET)
    user_id = request.user.id
    if not form.is_valid():
        logger.warning(form.errors)
        return _error_response(_DELETE_RESPONSE_PARAM)
    pk = form.cleaned_data["pk"]
    repo = FileRecordRepository()
    if not repo.is_own_file(pk, user_id):
        logger.warning(f"pk={pk} is not user_id={user_id} data.")
        return _error_response(_DELETE_RESPONSE_PARAM)
    repo.delete_file_record(pk, user_id)
    return redirect(f"/files?{_DELETE_RESPONSE_PARAM}=success")


@login_required
def file_download_view(request):
    form = FileSelectForm(request.GET)
    user_id = request.user.id
    if not form.is_valid():
        return _error_response(_DOWNLOAD_RESPONSE_PARAM)
    pk = form.cleaned_data["pk"]
    file_record = FileRecordRepository().get_file_record(pk, user_id)
    if not file_record:
        return _error_response(_DOWNLOAD_RESPONSE_PARAM)
    file_path = file_record.file_path
    try:
        return _streaming_download(file_record.file_name, file_path)
    except:
        logger.error(traceback.format_exc())
        return _error_response(_DOWNLOAD_RESPONSE_PARAM)


def _streaming_download(filename: str, file_path: str):
    return FileResponse(open(file_path, "rb"), as_attachment=True, filename=filename)


def _error_response(response_param: str):
    return redirect(f"/files?{response_param}=error")


def _get_paginator(request, data_count: int, paginate_by: int):
    paginator = Paginator([None for _ in range(data_count)], paginate_by)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj
