import os

class PostNlFileParser(object):
    def __init__(self, inputfile):
        self._f = open(inputfile, encoding="iso-8859-1")
        self._lines = []
        self._lines = self._f.readlines()
        self.raw_header, self.raw_documents, self.raw_footer = self.split_file(self._lines)
        self.doctype = self.determine_doctype(self.raw_header)
        self.documents = self.split_documents(self.raw_documents)
        broken_documents = self.documents
        fixed_documents = []
        for d in broken_documents:
            fixed_documents.append(self.fix_document(d))
        self.documents = fixed_documents

        

    @staticmethod
    def split_file(lines):
        header = []
        documents = []
        footer = []
        for l in lines:
            if l.startswith("A"):
                header.append(l)
            elif l.startswith("V"):
                documents.append(l)
            elif l.startswith("Z"):
                footer.append(l)
            else:
                raise ValueError("Invallid linestart: {}".format(l[0:1]))

        return header, documents, footer

    @staticmethod
    def determine_doctype(header):
        a040_found = False
        for l in header:
            if l.startswith("A040"):
                a040_found = True
                break
        if a040_found:
            return "16R"
        else:
            return "25R"

    @staticmethod
    def split_documents(raw_documents):
        documents = []
        new_document = []
        for l in raw_documents:
            if l.startswith("V010"):
                if len(new_document) > 0:
                    raise ValueError("New Document array was not empty! Is the inputfile syntactical correct?")
                new_document.append(l)
            elif l.startswith("V999"):
                new_document.append(l)
                documents.append(new_document)
                new_document = []
            else:
                new_document.append(l)
        return documents

    def fix_document(self, document):
        if self.doctype == "25R":
            required_lines = ["V010", "V020", "V035", "V040", "V050", "V060", "V070", "V080", "V081", "V090", "V091",
                              "V100", "V110", "V140", "V150", "V151", "V160", "V170", "V180", "V200", "V210", "V211",
                              "V212", "V213", "V999"]
        elif self.doctype == "16R":
            required_lines =  ["V010", "V020", "V035", "V040", "V050", "V060", "V070", "V080", "V081", "V090", "V091",
                               "V100", "V110", "V120", "V140", "V999"]
        else:
            raise ValueError("Unknown Documenttype {}".format(self.doctype))

        keys_in_documents = [l[0:4] for l in document]
        for req in required_lines:
            if req not in keys_in_documents:
                document.append(req + ' \n')
        return sorted(document)

    def save_as(self, filename):
        with open(filename, "w", encoding="iso-8859-1") as outfile:
            outfile.writelines(self.raw_header)
            for document in self.documents:
                outfile.writelines(document)
            outfile.writelines(self.raw_footer)

    def delete(self):
        self._f.close()
        f_path = self._f.name
        os.remove(f_path)

