from services.release_manifest_service import ReleaseManifestService


def test_create_manifest():

    manifest = ReleaseManifestService.create_manifest(
        version="1.2.0",
        release_name="Platform Integrity",
        architecture_status="Frozen",
        platform_status="Active",
        research_status="Candidate",
    )

    assert manifest.version == "1.2.0"
    assert manifest.release_name == "Platform Integrity"
    assert manifest.architecture_status == "Frozen"
    assert manifest.platform_status == "Active"
    assert manifest.research_status == "Candidate"