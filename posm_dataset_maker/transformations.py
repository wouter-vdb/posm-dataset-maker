from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from shutil import rmtree
from typing import Dict, List, Optional, Tuple
from xml.etree.cElementTree import ElementTree, parse

import environs

env = environs.Env()
env.read_env()  # read the .env file


LETTER_POS_TAG = "let"

# List of ignored files copied from
# https://github.com/konstantinosKokos/aethel/blob/stable/src/aethel/alpino/
IGNORED_FILES = {
    "WR-P-E-H-0000000050.p.3.s.1.xml",
    "WR-P-E-H-0000000036.p.3.s.1.xml",
    "WS-U-E-A-0000000027.p.3.s.1.xml",
    "WR-P-E-H-0000000052.p.3.s.1.xml",
    "wiki-356.p.22.s.1.xml",
    "wiki-356.p.20.s.1.xml",
    "WR-P-P-C-0000000049.txt-243.xml",
    "WS-U-E-A-0000000234.p.17.s.7.xml",
    "WR-P-E-H-0000000047.p.3.s.1.xml",
    "WS-U-E-A-0000000218.p.17.s.8.xml",
    "WS-U-E-A-0000000212.p.12.s.3.xml",
    "WR-P-E-H-0000000027.p.3.s.1.xml",
    "WS-U-E-A-0000000023.p.25.s.6.xml",
    "WR-P-P-I-0000000065.p.1.s.2.xml",
    "WR-P-P-I-0000000063.p.1.s.2.xml",
    "WR-P-P-I-0000000064.p.1.s.2.xml",
    "WS-U-E-A-0000000217.p.36.s.1.xml",
    "WR-P-E-H-0000000049.p.3.s.1.xml",
    "wiki-889.p.16.s.2.xml",
    "wiki-889.p.14.s.2.xml",
    "wiki-889.p.18.s.2.xml",
    "WR-P-P-I-0000000051.p.1.s.2.xml",
    "WR-P-P-I-0000000059.p.1.s.3.xml",
    "WR-P-P-C-0000000047.txt-52.xml",
    "WR-P-P-I-0000000049.p.1.s.2.xml",
    "WS-U-E-A-0000000222.p.28.s.11.xml",
    "WR-P-P-I-0000000057.p.1.s.2.xml",
    "WR-P-E-I-0000016944.p.3.s.288.xml",
    "WR-P-E-H-0000000013.p.3.s.1.xml",
    "WR-P-P-I-0000000068.p.1.s.2.xml",
    "WR-P-E-H-0000000020.p.3.s.1.xml",
    "WR-P-P-I-0000000050.p.1.s.2.xml",
    "wiki-135.p.16.s.1.xml",
    "WS-U-E-A-0000000045.p.1.s.2.xml",
    "WS-U-E-A-0000000045.p.2.s.2.xml",
    "WR-P-E-H-0000000040.p.3.s.1.xml",
    "WS-U-E-A-0000000225.p.34.s.2.xml",
    "WR-P-P-C-0000000062.p.167.s.2.xml",
    "WR-P-P-C-0000000062.p.39.s.1.xml",
    "WR-P-E-H-0000000055.p.3.s.1.xml",
    "WS-U-E-A-0000000031.p.1.s.2.xml",
    "WS-U-E-A-0000000031.p.2.s.2.xml",
    "WR-P-P-I-0000000062.p.1.s.2.xml",
    "WR-P-E-C-0000000036.p.32.s.1.xml",
    "WR-P-E-C-0000000036.p.58.s.1.xml",
    "WR-P-E-C-0000000036.p.41.s.1.xml",
    "WR-P-E-C-0000000036.p.97.s.1.xml",
    "WR-P-E-C-0000000036.p.101.s.1.xml",
    "WR-P-E-C-0000000036.p.147.s.1.xml",
    "WR-P-E-C-0000000036.p.18.s.1.xml",
    "WR-P-E-C-0000000036.p.65.s.1.xml",
    "WR-P-E-C-0000000036.p.100.s.1.xml",
    "WR-P-E-C-0000000036.p.145.s.1.xml",
    "WR-P-E-C-0000000036.p.74.s.1.xml",
    "WR-P-E-C-0000000036.p.106.s.1.xml",
    "WR-P-E-C-0000000036.p.44.s.1.xml",
    "WR-P-E-C-0000000036.p.56.s.1.xml",
    "WR-P-E-C-0000000036.p.120.s.1.xml",
    "WR-P-E-C-0000000036.p.112.s.1.xml",
    "WR-P-E-C-0000000036.p.109.s.1.xml",
    "WR-P-E-C-0000000036.p.77.s.1.xml",
    "WR-P-E-C-0000000036.p.68.s.1.xml",
    "WR-P-E-C-0000000036.p.99.s.1.xml",
    "WR-P-E-C-0000000036.p.35.s.1.xml",
    "WR-P-E-C-0000000036.p.48.s.1.xml",
    "WR-P-E-C-0000000036.p.88.s.1.xml",
    "WR-P-E-C-0000000036.p.38.s.1.xml",
    "WR-P-E-C-0000000036.p.29.s.1.xml",
    "WR-P-E-C-0000000036.p.95.s.1.xml",
    "WR-P-E-C-0000000036.p.139.s.1.xml",
    "WR-P-E-C-0000000036.p.23.s.1.xml",
    "WR-P-E-C-0000000036.p.87.s.1.xml",
    "WR-P-E-C-0000000036.p.60.s.1.xml",
    "WR-P-E-C-0000000036.p.96.s.1.xml",
    "WR-P-E-C-0000000036.p.144.s.1.xml",
    "WR-P-E-C-0000000036.p.59.s.1.xml",
    "WR-P-E-C-0000000036.p.146.s.1.xml",
    "WR-P-E-C-0000000036.p.21.s.1.xml",
    "WR-P-E-C-0000000036.p.103.s.1.xml",
    "WR-P-E-C-0000000036.p.19.s.1.xml",
    "WR-P-E-C-0000000036.p.57.s.1.xml",
    "WR-P-E-C-0000000036.p.80.s.1.xml",
    "WR-P-E-C-0000000036.p.98.s.1.xml",
    "WR-P-E-C-0000000036.p.24.s.1.xml",
    "WR-P-E-C-0000000036.p.85.s.1.xml",
    "WR-P-E-C-0000000036.p.115.s.1.xml",
    "WR-P-E-C-0000000036.p.61.s.1.xml",
    "WR-P-E-C-0000000036.p.22.s.1.xml",
    "WR-P-E-C-0000000036.p.49.s.1.xml",
    "WR-P-E-C-0000000036.p.46.s.1.xml",
    "WR-P-E-C-0000000036.p.20.s.1.xml",
    "WR-P-E-C-0000000036.p.63.s.1.xml",
    "WR-P-E-C-0000000036.p.143.s.1.xml",
    "WR-P-E-C-0000000036.p.26.s.1.xml",
    "WR-P-E-C-0000000036.p.71.s.1.xml",
    "WR-P-E-C-0000000036.p.83.s.1.xml",
    "WR-P-E-C-0000000036.p.118.s.1.xml",
    "WR-P-E-C-0000000036.p.62.s.1.xml",
    "WR-P-P-I-0000000056.p.1.s.2.xml",
    "WR-P-E-H-0000000009.p.3.s.1.xml",
    "WR-P-P-I-0000000053.p.1.s.2.xml",
    "wiki-5716.p.2.s.3.xml",
    "WR-P-E-H-0000000051.p.3.s.1.xml",
    "WR-P-P-I-0000000052.p.1.s.2.xml",
    "WR-P-P-I-0000000060.p.1.s.2.xml",
    "WR-P-P-I-0000000054.p.1.s.2.xml",
    "WR-P-E-C-0000000021.p.53.s.1.xml",
    "WR-P-E-C-0000000021.p.50.s.1.xml",
    "WR-P-E-C-0000000021.p.67.s.1.xml",
    "WR-P-E-C-0000000021.p.76.s.1.xml",
    "WR-P-E-C-0000000021.p.56.s.1.xml",
    "WR-P-E-C-0000000021.p.75.s.1.xml",
    "WR-P-E-C-0000000021.p.72.s.1.xml",
    "WR-P-E-C-0000000021.p.59.s.1.xml",
    "WR-P-E-C-0000000021.p.65.s.1.xml",
    "WR-P-E-C-0000000021.p.62.s.1.xml",
    "WR-P-E-C-0000000021.p.61.s.1.xml",
    "WR-P-E-C-0000000021.p.74.s.1.xml",
    "WR-P-E-C-0000000021.p.52.s.1.xml",
    "WR-P-E-C-0000000021.p.64.s.1.xml",
    "WR-P-E-C-0000000021.p.71.s.1.xml",
    "WR-P-E-C-0000000021.p.66.s.1.xml",
    "WR-P-E-C-0000000021.p.73.s.1.xml",
    "WR-P-E-C-0000000021.p.51.s.1.xml",
    "WR-P-E-C-0000000021.p.70.s.1.xml",
    "WR-P-E-C-0000000021.p.60.s.1.xml",
    "WR-P-E-C-0000000021.p.49.s.1.xml",
    "WR-P-E-C-0000000021.p.54.s.1.xml",
    "WR-P-E-C-0000000021.p.55.s.1.xml",
    "WR-P-E-C-0000000021.p.68.s.1.xml",
    "WR-P-E-C-0000000021.p.58.s.1.xml",
    "WR-P-E-C-0000000021.p.63.s.1.xml",
    "wiki-1617.p.27.s.2.xml",
    "WS-U-E-A-0000000020.p.44.s.8.xml",
    "WR-P-P-I-0000000058.p.1.s.3.xml",
    "WS-U-E-A-0000000025.p.40.s.9.xml",
    "WR-P-P-I-0000000066.p.1.s.2.xml",
    "WR-P-P-C-0000000051.txt-2.xml",
    "WR-P-P-C-0000000051.txt-308.xml",
    "WR-P-P-C-0000000051.txt-316.xml",
    "WR-P-P-C-0000000051.txt-64.xml",
    "WR-P-P-I-0000000067.p.1.s.2.xml",
    "wiki-1941.p.37.s.2.xml",
    "wiki-1941.p.33.s.2.xml",
    "wiki-1941.p.30.s.2.xml",
    "wiki-1941.p.28.s.2.xml",
    "wiki-1941.p.29.s.1.xml",
    "WR-P-P-I-0000000055.p.1.s.2.xml",
    "WR-P-P-G-0000000020.p.8.s.1.xml",
    "WR-P-P-I-0000000048.p.1.s.2.xml",
    "dpc-vla-001175-nl-sen.p.136.s.3.xml",
    "WS-U-E-A-0000000245.p.17.s.6.xml",
    "WS-U-E-A-0000000220.p.35.s.15.xml",
    "WS-U-E-A-0000000237.p.4.s.4.xml",
    "wiki-1941.p.5.s.1.xml",
    "dpc-kam-001286-nl-sen.p.10.s.2.xml",
    "WS-U-E-A-0000000211.p.17.s.9.4.xml",
    "wiki-7543.p.22.s.1.xml",
    "wiki-7543.p.22.s.2.xml",
}


class Extractor:
    def __init__(self, treebank_dir: Path, results_dir: Path) -> None:
        assert isinstance(treebank_dir, Path)
        assert isinstance(results_dir, Path)

        self.results_dir = results_dir
        self.treebank_dir = treebank_dir

        self.doc_cnt = 0
        self.snt_cnt = 0
        self.tag_set_nl = set()
        self.word_cnt = 0

        if results_dir.exists():
            rmtree(results_dir)
        results_dir.mkdir(parents=True)

    def extract_pos_dataset(
        self,
        include_letters: bool = True,
        results_indent: Optional[int] = None,
    ) -> None:
        pos_map: List[Tuple[str, str]]
        cnt = 0
        curr_doc = None
        curr_page = -1
        results = {}

        for doc_path in self.treebank_dir.iterdir():
            if doc_path.name.startswith("."):
                continue

            if not doc_path.is_dir():
                raise ValueError("Unexpected non-dir {}.".format(doc_path))

            doc_id = doc_path.name

            # Collect the POS-tagging results for the current doc:
            results = {}
            for tree_path in doc_path.iterdir():
                if tree_path.name[0] in {".", "#"}:
                    print(f"Skip {tree_path}")
                    continue

                if tree_path.name in IGNORED_FILES:
                    print(f"Skip {tree_path}")
                    continue

                if not tree_path.is_file():
                    raise ValueError("Unexpected non-file {}.".format(tree_path))

                name_parts = tree_path.name.split(".")
                sentence_id = ".".join(name_parts[1:-1])
                try:
                    etree = parse(tree_path)
                except Exception as error:
                    print(f"Failed to parse the tree in '{tree_path}'. {error}")
                    return
                sentence_data = self.extract_pos(
                    etree=etree,
                    doc=doc_id,
                    id=sentence_id,
                )
                results[sentence_id] = sentence_data
                self.snt_cnt += 1
                self.word_cnt += len(
                    [el for el in sentence_data["pos_nl"] if el[1] != LETTER_POS_TAG]
                )

            # Write the results file for the current doc:
            path = self.results_dir / f"{doc_id}.json"
            if path.exists():
                raise FileExistsError(path)
            with path.open("w") as file:
                json.dump(
                    {"doc": doc_id, "data": results},
                    file,
                    ensure_ascii=False,
                    indent=results_indent,
                    sort_keys=True,
                )
                file.write("\n")  # write an extra newline as per convention
            print(f"Wrote {path}")  # noqa: T201
            self.doc_cnt += 1

        # Write metadata:
        metadata = {
            "source": "Lassy Small",
            "all_tags": list(self.tag_set_nl),
            "document_count": self.doc_cnt,
            "sentence_count": self.snt_cnt,
            "word_count": self.word_cnt,
            "created_on": datetime.now().isoformat(),
        }
        path = self.results_dir / f"_metadata.json"
        with path.open("w") as file:
            json.dump(metadata, file, ensure_ascii=False, indent="  ")
            file.write("\n")  # write an extra newline as per convention

    def extract_pos(
        self,
        etree: ElementTree,
        doc: str,
        id: str,
        include_letters: bool = True,
    ) -> Dict[str, str | List[List[str, str]]]:
        """Extracts the sentence and the Parts-of-Speech mapping."""

        sentence = etree.find("./sentence").text

        pos_nl = []
        for node in etree.iter("node"):
            try:
                word = node.attrib["word"]
                word_idx = node.attrib["begin"]
                pos_tag = node.attrib["pt"]
                # print("  '{}': {}".format(word, pos_tag))
                if not include_letters and pos_tag == LETTER_POS_TAG:
                    # msg = "Found word '{}' with POS-tag 'let' in '{}'"
                    # print(msg.format(word, sentence))
                    continue
                self.tag_set_nl.add(pos_tag)
                pos_nl.append([int(word_idx), [word, pos_tag]])
            except KeyError:
                continue

        # Sort entries according to word index:
        pos_nl = [p2[1] for p2 in sorted(pos_nl, key=lambda p1: p1[0])]

        return {
            # "id": id,
            "sentence": sentence,
            "pos_nl": pos_nl,
        }


# def etree_to_dag(etree: ElementTree, name: str | None) -> DAG[str]:
#     nodes = set(etree.iter("node"))
#     edges = {
#         Edge(s.attrib["id"], t.attrib["id"], t.attrib["rel"])
#         for s in nodes
#         for t in s.findall("node")
#     }
#     attribs = {
#         n.attrib["id"]: {k: v for k, v in n.attrib.items() if k != "rel"}
#         for n in nodes
#     }
#     return DAG(
#         set(attribs.keys()), edges, attribs,
#         {"name": name} if name is not None else {}
#     )
