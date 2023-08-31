import sys
import urllib.request
import os
import os.path

remove_invalid_anchors = True
display_invalid_links = False

def processfile(fname):
    # print(f"Processing file: {fname}")
    # load the file's entire content
    content=open(fname).read()
    # accumulator for processed content
    content_processed=""
    # marker that the content was changed
    content_changed=False

    # find the first link
    link_pos=content.find("link:")
    while link_pos >= 0:
        # move everything before the link to processed
        content_processed+=content[:link_pos]
        content=content[link_pos:]

        # find the next [ and the next newline

        bracket=content.find("[")
        new_line=content.find("\n")

        # if the [ was not found or comes after the newline, this is not a valid link
        # in this case we output a warning
        if (bracket<0) or (new_line>0 and new_line<bracket):
            if display_invalid_links:
                print ("In file: "+fname)
                print ("Invalid link:")
            if new_line>0: # if there is a newline, the invalid link ends there
                if display_invalid_links:
                    print(content[:new_line])
                content_processed+=content[:new_line]
                content=content[new_line:]
            else: # if there is no newline, the invalid link is the entire remaining content
                if display_invalid_links:
                    print(content)
                content_processed+=content
                content=""
            # find the next link
            link_pos=content.find("link:")
            continue

        link_text=content[:bracket]
        content=content[bracket:]

        # if this link does not refer to d.o.c. container-platform, append to processed and continue

        if not link_text.startswith("link:https://docs.openshift.com/container-platform/latest"):
            content_processed+=link_text
            link_pos=content.find("link:")
            continue

        # exclude tkn_cli links
        if "tkn_cli" in link_text:
            content_processed+=link_text
            link_pos=content.find("link:")
            continue

        # if this link does not include a # , append to processed and continue

        if not ("#" in link_text):
            content_processed+=link_text
            link_pos=content.find("link:")
            continue

        # work out URL without the anchor
        url = link_text[len("link:"):]
        url = url[:url.find("#")]
        # print(url)
        url_body = str(urllib.request.urlopen(url).read())
        # print(url_body)
        anchor = link_text[link_text.find("#"):]
        #print(anchor)
        if url_body.find('<a class="anchor" href="'+anchor+'"')>=0:
            # print("anchor is valid")
            content_processed+=link_text

        #elif url_body.find(f'<a class="anchor" #href="{anchor}')>=0:
    #        print("auto-fixing anchor:")
#            print(link_text)
#            new_anchor = url_body[url_body.find(f'<a class="anchor" href="{anchor}'):]
#            new_anchor = new_anchor[new_anchor.find("#"):]
#            new_anchor = new_anchor[:new_anchor.find('"')]
#            new_link_text = "link:"+url+new_anchor
#            print(new_link_text)
        else:
            print(f"in file {fname} anchor is invalid:")
            print(link_text)
            if remove_invalid_anchors:
                new_link_text = "link:"+url
                content_processed+=new_link_text
                content_changed=True
                #print(url)
                #print(new_link_text)
                #print("!!!!!")
                #print(content_processed)
                #print("!!!!!")
                #print(content)
                #sys.exit()

        link_pos=content.find("link:")

    content_processed+=content
    if content_changed and remove_invalid_anchors:
        # rewrite the file with the new content
        open(fname,"w").write(content_processed)
        # pass



if len(sys.argv)<2:
    dir_path="."
else:
    dir_path=sys.argv[1]
for root, dirs, files in os.walk(dir_path):
    for file in files:
        if file.lower().endswith(".adoc"):
            processfile(os.path.join(root,file))
