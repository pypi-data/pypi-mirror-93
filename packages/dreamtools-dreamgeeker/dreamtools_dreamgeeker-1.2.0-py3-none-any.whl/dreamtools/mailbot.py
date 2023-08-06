# -*- coding: utf-8 -*-
# mailbot.py

"""
Module de Gestion de mail préparés

pathfile : dreamtools/mailbot.py

Pré-Requis
-------------
.. warning::

    Indiquer les parametres smtp dans le fichiers de configuration <PROJECT_NAME>/cfg/.app.yml

.. code-block:: YAML

    SMTP_HOST: smtp-host_adresse
    SMTP_PORT: port_smtp
    SMTP_AUTHMAIL: mail_authen
    SMTP_AUTHPWD: password_auth
    SMTP_USERNAME : name_sender <email>

.. warning::

    Les mails sont à définir dans le ficchier <PROJECT_NAME>/cfg/mailing.yml au format suivant

.. code-block:: YAML

     footer:
      html: <Pied de mail unique pour tous les mails (signature, rgpd...)>
      text: <Pied de mail unique pour tous les mails (signature, rgpd...)>
     code_mail:
      html: <ici mail au format HTML>
      text : <Le mail au format texte>
      objt : <Objet du mail>


"""
import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from . import cfgmng
from .logmng import CTracker as tracker


class CSMTP(object):
    SMTP_USERNAME : os.getenv('SMTP_USERNAME')
    SMTP_HOST: os.getenv('SMTP_HOST')
    SMTP_PORT: os.getenv('SMTP_PORT')
    SMTP_AUTHMAIL: os.getenv('SMTP_AUTHMAIL')
    SMTP_AUTHPWD: os.getenv('SMTP_AUTHPWD')
    SMTP_USERNAME: f"{os.getenv('SMTP_USERNAME')} {os.getenv('SMTP_AUTHMAIL')}"


class CMailer(CSMTP):
    footers = cfgmng.mailing_lib('footer')

    @classmethod
    def __send_mail(cls, subject, receivers, d_msg, to_receiver=None):
        """ Envoie du mail

        :param subject: Sujet du mail
        :param receivers: email destinataire
        :param d_msg: Message
        :param to_receiver: Nom destinataire
        :return:
        """

        tracker.flag("[dreamtools.mailbot] SEND_MAIL : Parametrage smtp")
        context = ssl.create_default_context()

        tracker.flag("[dreamtools.mailbot] SEND_MAIL:Parametrage message MIME")
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = cls.SMTP_USERNAME
        message["To"] = to_receiver or receivers

        tracker.flag("[dreamtools.mailbot] SEND_MAIL:Parametrage contenu mail")
        content = d_msg.get('text') + cls.footers['txt']
        content = MIMEText(content)
        message.attach(content)

        if d_msg.get('html'):
            content = d_msg.get('html') + cls.footers['html']
            content = MIMEText(content, "html")
            message.attach(content)

        tracker.flag("[dreamtools.mailbot] SEND_MAIL:Coonnexion SMTP")
        with smtplib.SMTP_SSL(cls.SMTP_HOST, cls.SMTP_PORT, context=context) as server:
            tracker.flag("[dreamtools.mailbot] SEND_MAIL:Authentification")
            server.login(cls.SMTP_AUTHMAIL, cls.SMTP_AUTHPWD)
            tracker.flag("[dreamtools.mailbot] SEND_MAIL: Sending")
            server.sendmail(cls.SMTP_AUTHMAIL, receivers, message.as_string())

            return True

    @classmethod
    def presend(cls, email, code, name='', **data_field):
        """ Preparation pour envoi d'un message mail 
        
        :param str email: email destinataire
        :param str code: réfénce du mail à chargé
        :param str name: nom du destinataire
        :param dict data_field: liste de données relatif à des champs définis dans le mails

        
        """
        tracker.flag('[dreamtools.mailbot] PRESEND:Loading template {}'.format(code))
        mail = cfgmng.mailing_lib(code)

        tracker.flag('[dreamtools.mailbot] PRESEND: Preparation')

        part1 = mail['text'].format(**data_field)
        part2 = mail['html'].format(**data_field)
        to_receiver = r'{} <{mail}>'.format(name, mail=email)

        tracker.flag('[dreamtools.mailbot] PRESEND: Envoi ({}) -> {}'.format(code, email))
        send = tracker.fntracker(cls.__send_mail, 'Envoi ({}) -> {}'.format(code, email), mail.get('object'),
                                 email, {'text': part1, 'html': part2}, to_receiver)

        return send.ok


__all__ = ['CMailer']
