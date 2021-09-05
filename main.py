import argparse
import os
import sys
from bs4 import BeautifulSoup

class ProfileLinkExtractor:

    def __init__(self):
        
        parser = argparse.ArgumentParser(description="A tool to extract a list of profile links from the HTML of a Facebook Event 'Guest List'")
        parser.add_argument("path", metavar="P", type=str, help="The path to the HTML file")
        parser.add_argument("--output_file", type=str, help="The output filename (.txt)")
        args = parser.parse_args()
        # Check that provided path is both an HTML file and that it actually exists
        if (args.path.split(".")[-1] != "html") or (not os.path.isfile(args.path)):
            raise sys.exit(f'"{args.path}" is not a valid path to an HTML file.')
        
        self.path = args.path
        self.links = []
        if args.output_file:
            self.out = args.output_file
        else:
            self.out = "output.txt"
        

    def extract_profile_links(self):
        with open(self.path, 'r', encoding="utf8") as f:
            soup = BeautifulSoup(f, "html.parser")
        
        # If this stopes working, Facebook probably changed the class names for this wrapper element
        # You will need to find the new class and update it here
        parent = soup.find('div', class_="b20td4e0 muag1w35")

        for child in parent.findChildren(recursive=False):
            self.links.append(child.next_element.attrs["href"])
        
        if not self.links:
            return "No links were able to be extracted from the input file."
        
        with open(self.out, "w", encoding="utf8") as f:
            for link in self.links:
                f.write(link + "\n")
        
        return f'{len(self.links)} links were extracted from the input file'


if __name__=="__main__":
    prog = ProfileLinkExtractor()
    print(prog.extract_profile_links())
