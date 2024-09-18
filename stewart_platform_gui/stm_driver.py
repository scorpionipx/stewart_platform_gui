import serial


class STMDriver:
    """
    STMDriver
    """
    def __init__(self, com_port, baud_rate=115200):
        """

        :param com_port: COM Port
        :type com_port: str
        """
        # connection
        # ==============================================================================================================
        self.__com_port = com_port
        self.__baud_rate = baud_rate

        self.__connected = False
        self.__connection = self.__connect()
        # ==============================================================================================================

    def __log_error(self, error):  # noqa
        """

        :param error:
        :return:
        """
        print(error)

    def __connection_required(method):  # noqa
        """

        :param method:
        :return:
        """
        def wrapper(self, *args, **kwargs):
            """

            :param self:
            :param args:
            :param kwargs:
            :return:
            """
            if not self.__connected:
                raise ConnectionError('A connection must be established first!')
            return method(self, *args, **kwargs)  # noqa

        return wrapper

    def __connect(self):
        """
        Establish connection.
        :return: connection
        :rtype: serial.Serial
        """
        if not self.__connected:
            try:
                connection = serial.Serial(
                    port=self.__com_port,
                    baudrate=self.__baud_rate,
                    timeout=None,
                    bytesize=8,
                    parity='N',
                    stopbits=1,
                )
                self.__connected = True
                return connection
            except Exception as exception:
                self.__connected = False
                error = f'Failed to establish connection: {exception}'
                self.__log_error(error)
                raise ConnectionError(error)

    def __disconnect(self):
        """
        Disconnect
        :return: None
        """
        if self.__connected:
            self.__connection.close()
            self.__connected = False

    def terminate(self):
        """
        Terminate application. To be called before closing.
        :return: None
        """
        self.__disconnect()

    @__connection_required  # noqa
    def __send_bytes(self, bytes_array):
        """
        Send specified bytes to the board.
        :param bytes_array: bytes array to be sent
        :type bytes_array: bytearray
        :return: None
        """
        self.__connection.write(bytes_array)

    def send_bytes(self, bytes_array):
        print(f'sb: {bytes_array}')
        return self.__send_bytes(bytes_array)

    @__connection_required  # noqa
    def __receive_bytes(self, expected_bytes=1):
        """
        Read bytes from the board.
        :param expected_bytes: number of expected bytes
        :type expected_bytes: int
        :return: received bytes
        :rtype: bytearray
        """
        return self.__connection.read(expected_bytes)

    @property
    def com_port(self):
        """
        Get COM Port.
        :return: com port
        :rtype: str
        """
        return self.__com_port

    @property
    def baud_rate(self):
        """
        Get baud rate.
        :return: baud_rate
        :rtype: int
        """
        return self.__baud_rate

    @property
    def connected(self):
        """
        Get connected status.
        :return: connected
        :rtype: bool
        """
        return self.__connected
