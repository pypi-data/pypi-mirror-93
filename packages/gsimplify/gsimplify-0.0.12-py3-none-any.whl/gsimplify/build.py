import gsimplify.auth
import tqdm
import os
import gsimplify.drive
import shutil
from googleapiclient.http import MediaIoBaseDownload
import gsimplify.templates
from typing import Union, List, Tuple
import git

from gsimplify.typedefs import FolderType


class Builder:
    def __init__(self, drive_str: str, template_dir: str, assets_dir: str = ""):
        self.drive_str = drive_str
        self.creds = gsimplify.auth.load_creds()
        self.drive = gsimplify.drive.Drive(drive_str, self.creds)
        self.templator = gsimplify.templates.Templates(template_dir)
        self.template_dir = template_dir
        self.assets_dir = assets_dir

        self.folders = self.drive.folders()
        self.file_tree = self.construct_folder_tree()
        self.navbar_items = self.construct_navbar()

    def adjust_relative_link(self, link: str):
        DRIVE_LINK_PREFIX = "https://docs.google.com/document/d/"
        DRIVE_LINK_END = "/"

        if DRIVE_LINK_PREFIX in link:
            doc_id = link.split(DRIVE_LINK_PREFIX)[1].split(DRIVE_LINK_END)[0]

            for each_file in self.drive.media(public=True):
                if doc_id == each_file.id:
                    path = f'{self.path_join(folder, "")}{doc.pointer.lower().replace(" ", "_")}'
                    break
            else:
                for doc in self.drive.docs(public=True):
                    if doc_id == doc.id:
                        for folder in self.drive.folders():
                            if folder.id == doc.parents:
                                break
                        else:
                            print("folder not found!")
                            return link

                        path = f'{self.path_join(folder, "")}{doc.pointer.lower().replace(" ", "_")}.html'
                        break


        return link

    @staticmethod
    def path_join(folder: gsimplify.typedefs.FolderType, prefix: str = "./build/"):
        return prefix + "/".join(folder.path).replace(" ","_").lower() + "/"

    def construct_folder_tree(
        self, path: list = [], start_folder: str = None
    ) -> list:
        """
        Recursively builds a folder tree.

        Note: This could be a contraction algo, but why bother?
        """
        if start_folder:
            pass
        elif self.folders:
            start_folder = self.drive_str
        else:
            return []

        level_folders = []  # all the folders within this level
        for each_folder in self.folders:
            if start_folder == each_folder.parents:
                each_folder.path = path + [each_folder.name]
                level_folders.append(
                    (
                        each_folder,
                        self.construct_folder_tree(
                            start_folder=each_folder.id, path=each_folder.path
                        ),
                    )
                )

        return level_folders

    def construct_navbar(self) -> List[Tuple[str, str]]:
        for doc in self.drive.docs():
            if doc.name == "Navbar":
                navbar = doc
                break
        else:
            print("Navbar not found!")  # TODO Handle this better
            return []

        gsimplify.docs.Docs(navbar, self.creds)

        sections = navbar.content['body']['content']

        navbar_items = []

        for section in sections:
            if 'paragraph' not in section:
                continue
            for element in section['paragraph']['elements']:
                if 'textRun' not in element:
                    continue
                if 'link' not in element['textRun']['textStyle']:
                    continue
                name = element['textRun']['content']
                link = element['textRun']['textStyle']['link']['url']
                navbar_items.append((name, self.adjust_relative_link(link)))

        return navbar_items

    def find_folder(
        self, folder: str
    ) -> Union[gsimplify.typedefs.DocType, gsimplify.typedefs.Drive]:
        if folder == self.drive_str:
            return gsimplify.typedefs.Drive()

        for each_folder in self.folders:
            if each_folder.id == folder:
                return each_folder

    def fetch_commit(self) -> str:
        """
        Fetches latest commit hash of repo.
        """
        repo = git.Repo(search_parent_directories=True)
        commit = repo.head.object.hexsha
        return commit[:6]

    def build(self, visual=True):
        """
        Loops and builds static website.
        """
        for each_doc in self.drive.docs(public=True):
            path = self.path_join(
                self.find_folder(each_doc.parents),
                prefix=f"./build/{self.fetch_commit()}",
            )

            if not os.path.exists("./build"):
                os.mkdir("./build")

            if not os.path.exists(path):
                os.mkdir(path)

            with open(path + each_doc.pointer.lower() + ".html", "w") as f:
                f.write(self.render(each_doc))

        for each_file in self.drive.media(public=True):
            path = self.path_join(
                self.find_folder(each_file.parents),
                prefix=f"./build/{self.fetch_commit()}/",
            )
            if not os.path.exists(path):
                os.mkdir(path)

            with open(path + each_file.pointer.lower().replace(" ", "_"), "wb") as f:
                file_handler = self.drive.service.files().get_media(fileId=each_file.id)
                downloader = MediaIoBaseDownload(f, file_handler)  # from google's docs

                if visual:
                    pbar = tqdm.tqdm(total=100)

                done = False
                while done is False:
                    status, done = downloader.next_chunk()

                    if visual:
                        pbar.update(int(status.progress()) * 100)

                if visual:
                    pbar.close()

        if self.assets_dir:
            if os.path.exists(f"./build/{self.fetch_commit()}/assets/"):
                shutil.rmtree(f"./build/{self.fetch_commit()}/assets/")
            shutil.copytree(self.assets_dir, f"./build/{self.fetch_commit()}/assets/")

        shutil.rmtree("./build/latest", ignore_errors=True)
        shutil.copytree(f"./build/{self.fetch_commit()}", "./build/latest")


    def render(self, doc, template="example.html"):
        document = gsimplify.docs.Docs(doc, self.creds, self.navbar_items, self)
        return document.render(self.templator.get("example.html"))
