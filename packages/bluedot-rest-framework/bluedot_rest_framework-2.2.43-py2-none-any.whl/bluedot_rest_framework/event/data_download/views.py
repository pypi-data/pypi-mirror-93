import requests
from rest_framework import status
from email.utils import formataddr
from django.conf import settings
from rest_framework.response import Response
from django.core.mail import send_mail
from django.core.mail.message import EmailMessage
from rest_framework.decorators import action
from bluedot_rest_framework import import_string
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet
from bluedot_rest_framework.utils.crypto import AESEncrypt
from bluedot_rest_framework.utils.jwt_token import jwt_get_wechatid_handler, jwt_get_userid_handler
from bluedot_rest_framework.event.frontend_views import FrontendView


EventRegister = import_string('event.register.models')
EventDataDownload = import_string('event.data_download.models')
EventDataDownloadSerializer = import_string('event.data_download.serializers')


class EventDataDownloadView(CustomModelViewSet, FrontendView):
    model_class = EventDataDownload
    serializer_class = EventDataDownloadSerializer
    pagination_class = None
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        event_id = request.query_params.get('event_id', None)
        queryset = self.model_class.objects.filter(event_id=event_id).first()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        queryset = self.model_class.objects.filter(
            event_id=request.data.get('event_id', None)).first()
        if queryset:
            partial = kwargs.pop('partial', False)
            serializer = self.get_serializer(
                queryset, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['post'], url_path='send-email', url_name='send-email')
    def send_email(self, request, *args, **kwargs):
        data_list = request.data["data"]
        wechat_id = jwt_get_wechatid_handler(request.auth)
        if wechat_id == 0:
            userid = jwt_get_userid_handler(request.auth)
            email = EventRegister.objects.filter(userid=userid).first().email
        else:
            email = EventRegister.objects.filter(
                wechat_id=wechat_id).first().email
        email = AESEncrypt.decrypt(email)

        html_content = '<table width="800" border="0" align="center" cellspacing="0" cellpadding="0"><tbody><tr><td width="33"></td><td colspan="2" valign="bottom"><img src="https://spgchinaratings.oss-cn-beijing.aliyuncs.com/mi/img/miniprogram/post_logo_mi.png" style="width:40%;max-width:150px;margin-bottom:10px;/></td><td width="33"></td></tr>'
        html_content += '<tr><td width="33"></td><td colspan="2" height="50" valign="bottom" style="color:#34454f; font-size:16px;">感谢您的关注。您可以在本封邮件内下载您所需要的资料。</td><td width="33"></td></tr>'
        html_content += '</tr><tr><td width="33"></td><td colspan="2" valign="bottom" width="744" height="50" style="color:#c52933; font-size:20px;">请通过下方地址进行下载。</td><td width="33"></td></tr>'
        html_content += '<tr><td width="33" height="50"></td><td width="734" colspan="2"><img src="http://flender.blue-dot.cn/view/templates/Home/images/line.jpg"/></td><td width="33"></td></tr>'
        for i in data_list:
            html_content += f'<tr><td width="33"></td><td colspan="2" height="50" valign="bottom" style="color:#34454f; font-size:16px;font-weight: bold;"><a href="{i["url"]}" style="text-decoration:underline">{i["title"]}</a></td><td width="33"></td>'
        html_content += '</tbody></table>'

        from_email = formataddr(
            pair=(settings.EMAIL_FROM_NAME, settings.EMAIL_HOST_USER))
        send_mail(subject='【下载资料】',
                  message='',
                  html_message=html_content,
                  from_email=from_email,
                  recipient_list=[email])
        return Response()
