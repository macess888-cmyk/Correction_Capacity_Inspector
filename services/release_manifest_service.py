from models.release_manifest import ReleaseManifest


class ReleaseManifestService:
    """
    Service responsible for creating Release Manifest objects.

    The service contains no UI logic and no persistence logic.
    """

    @staticmethod
    def create_manifest(
        version: str,
        release_name: str,
        architecture_status: str,
        platform_status: str,
        research_status: str,
    ) -> ReleaseManifest:

        return ReleaseManifest(
            version=version,
            release_name=release_name,
            architecture_status=architecture_status,
            platform_status=platform_status,
            research_status=research_status,
        )