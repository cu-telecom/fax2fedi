# fax2fedi

After the huge success of [fax2tweet](https://github.com/cu-telecom/fax2tweet) we now bring you fax2fedi!

Takes a PDF, converts the first page into a PNG and then toots it. The intended use is converting faxes into Toots with Asterisk.

It's an unpolished proof of concept. But should get you started.

## Usage

    fax2fedi.py [Path to PDF] [Text to Tweet]
 
### Requirements

You need python3, the modules in requirements.txt, and the `libtiff-tools` and `poppler-utils` packages.

You also need to create an "application" on your Mastodon server  (`preferences` > `development`) 

### Env Vars

Mastodon API creds are supplied as env vars. They're self explanatory:

MASTODON_CLIENT_KEY  
MASTODON_CLIENT_SECRET  
MASTODON_ACCESS_TOKEN  
MASTODON_API_BASE_URL  

## Asterisk Config

    [recv-fax]
    exten => s,1,Noop("Connected to recv-fax")
    same => n,Answer()
    same => n,Set(TWEETTEXT=Fax from ${CALLERID(number)})
    same => n,Set(FAXDEST=/tmp/faxes)
    same => n,Set(FAXNAME=${STRFTIME(,,%C%y%m%d%H%M)})
    same => n,Set(FAXPATH=${FAXDEST}${FAXNAME})
    same => n,ReceiveFax(${FAXPATH}.tif)
    same => n,Noop(Converting tif to pdf)
    same => n,Set(TIFF2PDF=${SHELL(tiff2pdf ${FAXPATH}.tif -o ${FAXPATH}.pdf)})
    same => n,Noop(Sending Toot)
    same => n,Noop(PDF Path: ${FAXPATH}.pdf)
    same => n,Set(FAX2TWEET=${SHELL(python3 -u /var/lib/asterisk/bin/fax2fedi.py ${FAXPATH}.pdf "${TWEETTEXT}" >> /tmp/log)})
    same => n,Noop(Deleting old file)
    same => n,Set(DELETE=${SHELL(rm ${FAXPATH}*)})
    same => n,Wait(30)
    same => n,Hangup()
  
## Disclaimers

This is a lash up to get it working. Use at your own risk!

## Licence 

This project is licenced under the MIT license. See LICENSE for details

