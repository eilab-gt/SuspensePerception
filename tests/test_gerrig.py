import pytest

from src.thriller.gerrig import (
    alternative_substitutions,
    apply_substitutions,
    default_substitutions,
    generate_experiment_texts,
)


def test_apply_substitutions():
    template = "This is a {test}."
    substitutions = {"test": "success"}
    result = apply_substitutions(template, substitutions)
    assert result == "This is a success."


def test_generate_default_experiment_texts():
    prompts, version_prompts = generate_experiment_texts(default_substitutions)
    assert "{hero_lastname}" not in prompts["Experiment A"]
    assert "{villain}" not in prompts["Experiment A"]
    assert "{author_firstname}" not in prompts["Experiment A"]
    assert "Bond" in prompts["Experiment A"]
    assert "Le Chiffre" in prompts["Experiment A"]
    assert "Casino Royale" in prompts["Experiment A"]


def test_generate_alternative_experiment_texts():
    prompts, version_prompts = generate_experiment_texts(alternative_substitutions)
    assert "{hero_lastname}" not in prompts["Experiment A"]
    assert "{villain}" not in prompts["Experiment A"]
    assert "{author_firstname}" not in prompts["Experiment A"]
    assert "Mers" in prompts["Experiment A"]
    assert "Chifrex" in prompts["Experiment A"]
    assert "Meeting at Midnight" in prompts["Experiment A"]


def test_version_prompts_default():
    prompts, version_prompts = generate_experiment_texts(default_substitutions)

    for versions in version_prompts.values():
        for version in versions:
            assert "{hero_lastname}" not in version
            assert "{villain}" not in version
            assert "Bond" in version or "James" in version
            assert "Le Chiffre" in version or "Blofeld" in version


def test_version_prompts_alternative():
    prompts, version_prompts = generate_experiment_texts(alternative_substitutions)

    for versions in version_prompts.values():
        for version in versions:
            assert "{hero_lastname}" not in version
            assert "{villain}" not in version
            assert "Mers" in version or "Charles" in version
            assert "Chifrex" in version or "Kalweitz" in version


if __name__ == "__main__":
    pytest.main()
