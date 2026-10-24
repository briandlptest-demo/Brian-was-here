# CLASSIFICATION: INTERNAL // RESTRICTED // ASPEN-COMPARTMENTED
import pytest

from aspen import Colony, ColonyConfig, ContainmentBreach, ContainmentPolicy, Genome
from aspen.rhizome import Rhizome


@pytest.fixture(autouse=True)
def _no_firebreak(monkeypatch, tmp_path):
    monkeypatch.delenv("ASPEN_FIREBREAK", raising=False)
    monkeypatch.setattr("aspen.containment.KILL_SWITCH_FILE", tmp_path / "firebreak")


def test_colony_starts_as_single_seedling():
    colony = Colony()
    assert len(colony.ramets) == 1


def test_colony_grows_under_demand():
    colony = Colony()
    colony.grow(15)
    assert len(colony.ramets) > 1
    assert colony.rhizome.total_deposited > 0


def test_all_ramets_share_one_genome():
    colony = Colony()
    colony.grow(10)
    assert {r.genome.fingerprint for r in colony.ramets} == {colony.genome.fingerprint}


def test_containment_ceiling_is_never_exceeded():
    cfg = ColonyConfig(containment=ContainmentPolicy(max_ramets=10), demand_growth=0.5)
    colony = Colony(cfg)
    colony.grow(30)
    assert all(r.ramets <= 10 for r in colony.history)


def test_firebreak_halts_growth(monkeypatch):
    monkeypatch.setenv("ASPEN_FIREBREAK", "1")
    with pytest.raises(ContainmentBreach):
        Colony().step()


def test_invalid_growth_token_rejected():
    cfg = ColonyConfig(containment=ContainmentPolicy(growth_token="letmein"))
    with pytest.raises(ContainmentBreach):
        Colony(cfg).step()


def test_rhizome_survives_total_fire():
    colony = Colony()
    colony.grow(15)
    before = colony.rhizome.total_deposited
    colony.fire(severity=1.0)
    assert colony.rhizome.total_deposited == before
    assert len(colony.ramets) == 1  # regrown from the roots


def test_rich_rhizome_gives_stronger_sprouts():
    rhizome = Rhizome(["code"])
    weak = rhizome.sprout_bonus("code", 0.35)
    rhizome.deposit("code", 500)
    assert rhizome.sprout_bonus("code", 0.35) > weak


def test_expression_weights_sum_to_one():
    weights = Genome().expression_weights("code")
    assert sum(weights.values()) == pytest.approx(1.0)
    assert max(weights, key=weights.get) == "code"
