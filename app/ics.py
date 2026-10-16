import win32com.client


def list_connections():
    """Return the names of network connections visible to ICS."""
    net_share = win32com.client.Dispatch("HNetCfg.HNetShare")

    connections = []

    for connection in net_share.EnumEveryConnection:
        properties = net_share.NetConnectionProps(connection)
        connections.append(properties.Name)

    return sorted(connections, key=str.casefold)


def configure_ics(source_name, target_name):
    """
    Configure Internet Connection Sharing.

    The source connection is configured as public.
    The target connection is configured as private.

    Existing ICS configurations are saved before being changed.
    If the operation fails, the previous configuration is restored
    on a best-effort basis.
    """
    if not source_name or not target_name:
        raise ValueError(
            "Select both the VPN and hotspot connections."
        )

    if source_name == target_name:
        raise ValueError(
            "The source and target connections must be different."
        )

    net_share = win32com.client.Dispatch("HNetCfg.HNetShare")

    connections = []
    source_conn = None
    target_conn = None

    # Locate and validate both connections before changing anything.
    for connection in net_share.EnumEveryConnection:
        properties = net_share.NetConnectionProps(connection)
        connections.append(connection)

        if properties.Name == source_name:
            source_conn = connection

        if properties.Name == target_name:
            target_conn = connection

    if source_conn is None:
        raise RuntimeError(
            f"Source connection not found: {source_name}"
        )

    if target_conn is None:
        raise RuntimeError(
            f"Target connection not found: {target_name}"
        )

    # Obtain configuration objects and save the original ICS state.
    configurations = []
    previous_states = []

    for connection in connections:
        config = (
            net_share.INetSharingConfigurationForINetConnection(
                connection
            )
        )

        configurations.append((connection, config))

        properties = net_share.NetConnectionProps(connection)
        connection_name = properties.Name

        try:
            sharing_enabled = config.SharingEnabled

            if sharing_enabled:
                sharing_type = config.SharingConnectionType

                previous_states.append(
                    (connection, sharing_type)
                )

        except Exception as error:
            raise RuntimeError(
                "Could not read the existing Internet Connection "
                "Sharing configuration.\n\n"
                f"Connection: {connection_name}\n"
                f"Property: SharingEnabled/SharingType\n"
                f"Windows error: {error}"
            ) from error

    try:
        # Disable existing sharing configurations.
        for _, config in configurations:
            if config.SharingEnabled:
                config.DisableSharing()

        # Enable sharing on the selected source and target.
        source_config = (
            net_share.INetSharingConfigurationForINetConnection(
                source_conn
            )
        )

        target_config = (
            net_share.INetSharingConfigurationForINetConnection(
                target_conn
            )
        )

        source_config.EnableSharing(0)  # Public connection
        target_config.EnableSharing(1)  # Private connection

    except Exception as original_error:
        # Attempt to restore the previous sharing configuration.
        restoration_errors = []

        try:
            # Disable any sharing created by the failed operation.
            for _, config in configurations:
                try:
                    if config.SharingEnabled:
                        config.DisableSharing()
                except Exception as error:
                    restoration_errors.append(
                        f"Could not disable sharing: {error}"
                    )

            # Restore the previous public/private connections.
            for connection, sharing_type in previous_states:
                try:
                    config = (
                        net_share
                        .INetSharingConfigurationForINetConnection(
                            connection
                        )
                    )

                    config.EnableSharing(sharing_type)

                except Exception as error:
                    restoration_errors.append(
                        f"Could not restore a previous connection: "
                        f"{error}"
                    )

        except Exception as restoration_error:
            restoration_errors.append(str(restoration_error))

        if restoration_errors:
            details = "\n".join(
                f"- {error}" for error in restoration_errors
            )

            raise RuntimeError(
                "ICS configuration failed, and the previous "
                "configuration could not be fully restored.\n\n"
                f"Original error: {original_error}\n\n"
                f"Restoration errors:\n{details}"
            ) from original_error

        raise RuntimeError(
            "ICS configuration failed. The previous sharing "
            "configuration was restored.\n\n"
            f"Error: {original_error}"
        ) from original_error