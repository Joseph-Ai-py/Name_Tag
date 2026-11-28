# NAME TAG experiments and historical references

- `streamlit/`: original Streamlit MVP (24 files); run from this directory in its own environment.
- `streamlit/v2/`: conversational experiment (8 text files); placed directly under the V1 directory as expected by its import paths. Original gitlink is not imported. Run from `experiments/streamlit` using `python -m streamlit run v2/app.py --server.port 8504` after installing the V1 dependencies; runtime not verified.
- `legacy-tests/`: historical notebooks and test documentation. Generated PDF is not imported. Not part of active test suite.
- `legacy-backup/`: selected prior implementation reference files, NOT a full runnable backup. Keep original repository until a full history backup is made.
- [Name_Tag_V2](https://github.com/Joseph-Ai-py/Name_Tag_V2) stays separate: persistent agent workspace and research architecture needs integration design and runtime tests.

Original sources: [Streamlit](https://github.com/Joseph-Ai-py/Name_Tag_Streamlit), [Streamlit V2](https://github.com/Joseph-Ai-py/Name_Tag_Streamlit_V2), [Test](https://github.com/Joseph-Ai-py/Name_Tag_Test_Repository), [Backup](https://github.com/Joseph-Ai-py/Name_Tag_backup).

This is source consolidation, not production integration. Existing application source unchanged. Basic secret-pattern scan only; review notebooks and ownership before deleting originals. No execution tests performed.

Skipped by basic scan or fetch: []
