# NAME TAG experiments and historical references

- `streamlit/`: original Streamlit MVP (24 files); run from this directory in its own environment.
- `streamlit/v2/`: conversational experiment (8 text files); placed directly under the V1 directory as expected by its import paths. Original gitlink is not imported (`Name_Tag_V2_temp`, commit `3a827546cd4a403b7851ebf4f612cc5b3f2c4b7e`); retain the source until its provenance and contents are verified. Run from `experiments/streamlit` using `python -m streamlit run v2/app.py --server.port 8504` after installing the V1 dependencies; runtime not verified.
- `legacy-tests/`: historical notebooks and test documentation. Generated PDF has now been imported byte-for-byte and its Git blob SHA matches the original. Not part of active test suite.
- `legacy-backup/`: selected prior implementation reference files, NOT a full runnable backup. Keep original repository until a full history backup is made; 7 of 96 original blobs currently match the destination, and the source also contains a `past` gitlink.
- [Name_Tag_V2](https://github.com/Joseph-Ai-py/Name_Tag_V2) stays separate: persistent agent workspace and research architecture needs integration design and runtime tests.

Original sources: [Streamlit](https://github.com/Joseph-Ai-py/Name_Tag_Streamlit), [Streamlit V2](https://github.com/Joseph-Ai-py/Name_Tag_Streamlit_V2), [Test](https://github.com/Joseph-Ai-py/Name_Tag_Test_Repository), [Backup](https://github.com/Joseph-Ai-py/Name_Tag_backup).

This is source consolidation, not production integration. Existing application source unchanged. Basic secret-pattern scan only; review notebooks and ownership before deleting originals. No execution tests performed.

Skipped by basic scan or fetch: []


Update 2026-11-28: all 10 legacy test blobs and all 24 original Streamlit blobs now match the source; all 8 conversational Streamlit blobs match, excluding the unresolved gitlink. Git history is not migrated. Runtime QA is not certified.
