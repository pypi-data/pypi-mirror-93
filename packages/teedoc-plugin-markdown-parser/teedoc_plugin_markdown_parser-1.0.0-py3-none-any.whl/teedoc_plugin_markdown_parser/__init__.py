import os, sys
import markdown2
try:
    curr_path = os.path.dirname(os.path.abspath(__file__))
    teedoc_project_path = os.path.abspath(os.path.join(curr_path, "..", "..", ".."))
    if os.path.basename(teedoc_project_path) == "teedoc":
        sys.path.insert(0, teedoc_project_path)
except Exception:
    pass
from teedoc import Plugin_Base
from teedoc import Fake_Logger



class Plugin(Plugin_Base):
    name = "markdown-parser"
    desc = "markdown parser plugin for teedoc"
    defautl_config = {
        "parse_files": ["md"]
    }

    def __init__(self, config = {}, doc_src_path = ".", logger = None):
        '''
            @config a dict object
            @logger teedoc.logger.Logger object
        '''
        self.logger = Fake_Logger() if not logger else logger
        self.doc_src_path = doc_src_path
        self.config = Plugin.defautl_config
        self.config.update(config)
        self.logger.i("-- plugin <{}> init".format(self.name))
        self.logger.i("-- plugin <{}> config: {}".format(self.name, self.config))
        self._extention = [
            "toc",
            "metadata",
            "fenced-code-blocks",
            "highlightjs-lang",
            "break-on-newline",
            "code-friendly",
            "cuddled-lists",
            "footnotes",
            "strike",
            "spoiler",
            "tables",
            "task_list"
        ]
        self.parser = markdown2.Markdown(extras = self._extention)
        

    def on_parse_files(self, files):
        # result, format must be this
        result = {
            "ok": False,
            "msg": "",
            "htmls": {}
        }
        # function parse md file is disabled
        if not "md" in self.config["parse_files"]:
            result["msg"] = "disabled markdown parse, but only support markdown"
            return result
        self.logger.d("-- plugin <{}> parse {} files".format(self.name, len(files)))
        # self.logger.d("files: {}".format(files))
        
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext.endswith("md"):
                with open(file, encoding="utf-8") as f:
                    content = f.read().strip()
                    self.parser._toc_html = ""
                    html = self.parser.convert(content)
                    if "title" in html.metadata:
                        title = html.metadata["title"]
                    else:
                        title = ""
                    if "keywords" in html.metadata:
                        keywords = html.metadata["keywords"].split(",")
                    else:
                        keywords = []
                    if "tags" in html.metadata:
                        tags = html.metadata["tags"].split(",")
                    else:
                        tags = []
                    if "desc" in html.metadata:
                        desc = html.metadata["desc"]
                    else:
                        desc = []
                    result["htmls"][file] = {
                        "title": title,
                        "desc": desc,
                        "keywords": keywords,
                        "tags": tags,
                        "body": html,
                        "toc": html.toc_html if html.toc_html else "",
                        "metadata": html.metadata
                    }
            else:
                result["htmls"][file] = None
        result['ok'] = True
        return result
    
    def on_parse_pages(self, files):
        print(files)
        result = self.on_parse_files(files)
        print(result)
        return result

    
    def on_add_html_header_items(self):
        items = []
        items.append('<meta name="markdown-generator" content="teedoc-plugin-markdown-parser">')
        return items

if __name__ == "__main__":
    config = {
    }
    plug = Plugin(config=config)
    res = plug.parse_files(["md_files/basic.md"])
    print(res)
    if not os.path.exists("out"):
        os.makedirs("out")
    for file, html in res["htmls"].items():
        if html:
            file = "{}.html".format(os.path.splitext(os.path.basename(file))[0])
            with open(os.path.join("out", file), "w") as f:
                f.write(html)

