from pathlib import Path

import environs

from posm_dataset_maker.transformations import Extractor

env = environs.Env()
env.read_env()  # read the .env file

INCLUDE_LETTER_POS_TAGS = env.bool("INCLUDE_LETTER_POS_TAGS", True)
RESULTS_INDENT = env.int("RESULTS_INDENT", None)


def main():
    treebank_dir = env.path("TREEBANK_DIR").resolve()
    results_dir = Path("results/posm_dataset_lassy_small_v1/").resolve()
    extractor = Extractor(treebank_dir=treebank_dir, results_dir=results_dir)
    extractor.extract_pos_dataset(
        include_letters=INCLUDE_LETTER_POS_TAGS,
        results_indent=RESULTS_INDENT,
    )


if __name__ == "__main__":
    main()
