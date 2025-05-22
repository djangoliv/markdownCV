import os.path
import sys


def personal_info_from_md_line(txt):
    """Return personal info for lines with links
    e.g.
    input:  "`email`    [abc@example.com](mailto:abc@example.com)"
    output: "abc@example.com"
    """
    txt = txt.split("[")[1]
    txt = txt.split("]")[0]
    return txt


def split_cv_line(txt):
    """Return a tuple of the side bar text and title
    e.g.
    input:  "*Gen 2000 -- Dec 2020* Example GmbH -- Intern"
    output: ("Gen 2000 -- Dec 2020", "Example GmbH -- Intern")
    """
    if "*" not in txt:
        return "", txt

    txt = txt.split("*", 1)[1]
    txt = txt.split("*")
    side_text = txt[0].strip()
    title = txt[1].strip()
    return side_text, title


class CvSection:
    def __init__(self, title):
        self.title = title

    def to_tex(self):
        return f"\\section{{{self.title}}}"


class CvEntry:
    def __init__(self, side_txt, title):
        self.side_txt = side_txt
        self.title = title

    def to_tex(self):
        return f"\\cventry{{{self.side_txt}}}{{{self.title}}}{{}}{{}}{{}}{{}}"


class CvItem:
    def __init__(self, side_txt, title):
        self.side_txt = side_txt
        self.title = title

    def to_tex(self):
        title = self.title
        if title.startswith("-"):
            title = "--" + title[1:]
        return "\\cvitem{{{}}}{{{}}}".format(self.side_txt, title)


class EmptyLine:
    def to_tex(self):
        return "\\vspace{0.3cm}"


class CurriculumVitae:
    def __init__(self, language="english"):
        self.language = language
        self.name = None
        self.title = None
        self.content = None
        self.photo = None
        self.homepage = None
        self.linkedin = None
        self.content = []

    def from_markdown(self, markdown_src):
        for line in markdown_src.splitlines():
            if line.startswith("# "):
                line = line.removeprefix("# ")
                self.name, self.title = line.split("-")
            elif line.startswith("![]"):
                self.photo = line.split("(")[1].split(")")[0]
            elif line.startswith("`email`"):
                self.email = personal_info_from_md_line(line)
            elif line.startswith("`homepage`"):
                self.homepage = personal_info_from_md_line(line)
            elif line.startswith("`linkedin`"):
                self.linkedin = personal_info_from_md_line(line)
            elif line.startswith("`github`"):
                self.github = personal_info_from_md_line(line)
            elif line.startswith("`address`"):
                self.address = personal_info_from_md_line(line)
            elif line.startswith("`phone`"):
                self.phone = personal_info_from_md_line(line)
            elif line.startswith("`extrainfo`"):
                self.extrainfo = personal_info_from_md_line(line)
            elif line.startswith("## "):
                self.content.append(CvSection(line.removeprefix("## ")))
            elif line.startswith("### "):
                txt = line.removeprefix("### ")
                side_text, title = split_cv_line(txt)
                self.content.append(CvEntry(side_text, title))
            elif line.strip() == "_":
                self.content.append(EmptyLine())
            elif line.strip() != "":
                side_text, title = split_cv_line(line)
                self.content.append(CvItem(side_text, title))

    def personal_data_to_tex(self):
        tex_out = []
        tex_out.append(f"\\name {{{self.name.split()[0]}}}{{{self.name.split()[1]}}}")
        if self.title is not None:
            tex_out.append(f"\\title{{{self.title}}}")
        if self.photo is not None:
            tex_out.append("\\photo[80pt][0pt]{{{}}}".format(self.photo))
        if self.email is not None:
            tex_out.append("\\email{{{}}}".format(self.email))
        if self.homepage is not None:
            tex_out.append("\\homepage{{{}}}".format(self.homepage))
        if self.linkedin is not None:
            tex_out.append("\\social[linkedin]{{{}}}".format(self.linkedin))
        if self.github is not None:
            tex_out.append("\\social[github]{{{}}}".format(self.github))
        if self.phone is not None:
            tex_out.append("\\phone{{{}}}".format(self.phone))
        if self.address is not None:
            tex_out.append("\\address{{{}}}".format(self.address))
        if self.extrainfo is not None:
            tex_out.append("\\extrainfo{{{}}}".format(self.extrainfo))

        tex_out = "\n".join(tex_out)
        return tex_out

    def content_to_tex(self):
        content_lines = [item.to_tex() for item in self.content]
        return "\n".join(content_lines)

    def to_tex(self):
        tex_template = open("cv_template.tex", "rt").read()
        tex_template = tex_template.replace("$language", self.language)
        tex_template = tex_template.replace(
            "$personal_data", self.personal_data_to_tex()
        )
        tex_template = tex_template.replace("$content", self.content_to_tex())
        return tex_template


if __name__ == "__main__":
    src_filename = sys.argv[1]
    if len(sys.argv) > 2:
        language = sys.argv[2]
    else:
        language = None
    cv = CurriculumVitae(language)
    cv.from_markdown(open(src_filename, "rt").read())
    open(os.path.splitext(src_filename)[0] + ".tex", "wt").write(cv.to_tex())
