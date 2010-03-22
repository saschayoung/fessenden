class data_utils:


    def __init__(self):
        self.rx_location = []
        self.rx_time_delay = []
        self.rx_team_id = []
        self.rx_power = []
        self.rpt_packet = []


    def reset_rx_location(self):
        self.rx_location = []

    # setters
    ###########################################################################
    def set_tx_location(self,coords):
        """
        set tx_location.
        used at start of simulation.
        """
        self.tx_location = coords
        
    def set_rx_number(self,n):
        """
        set number of receivers n to be used in simulation.
        used at start of simulation
        """        
        self.rx_number = n

    def set_rx_location(self,coords):
        """
        set locations for n receivers at start of simulation.
        used at start of simulation.
        """
        self.rx_location.append(coords)        

    def set_timestamp_base(self,t):
        """
        set common/base time value to which individual repeater
        time delays are added to create time of arrival time stamp
        that is somewhat common clock synchronized
        """
        self.timestamp_base = t

    def set_rx_time_delay(self,delay):
        """
        set time of arrival delay (actually time of flight) for packet n
        """
        self.rx_time_delay.append(delay)

    def set_rx_team_id(self,ident):
        """
        set team id for all teams.
        used at start of simulation.
        """
        self.rx_team_id.append(ident)

    def set_rx_power(self,power):
        """
        set rx power level at repeater n
        """
        self.rx_power.append(power)

    def set_beacon_packet(self,packet):
        """
        set/save received beacon packet
        """
        self.beacon_packet = packet

    def set_rpt_packet(self,packet):
        """
        set/save repeater packet for repeater n
        """
        self.rpt_packet.append(packet)
    ###########################################################################


    # getters
    ###########################################################################
    def get_tx_location(self):
        """
        get tx_location.
        """
        return self.tx_location

    def get_rx_number(self):
        """
        return number of receivers n used in simulation
        """
        return self.rx_number

    def get_rx_location(self):
        """
        get location of repeaters
        """
        return self.rx_location

    def get_timestamp_base(self):
        """
        get common/base time value to which individual repeater
        time delays are added to create time of arrival time stamp
        that is somewhat common clock synchronized
        """ 
        return self.timestamp_base

    def get_rx_time_delay(self):
        """
        get time of arrival delay (actually time of flight)
        """
        return self.rx_time_delay

    def get_rx_team_id(self):
        """
        get team ids
        """
        return self.rx_team_id
    
    def get_rx_power(self):
        """
        get rx power levels
        """
        return self.rx_power

    def get_beacon_packet(self):
        """
        get received beacon packet (from internal memory)
        """
        return self.beacon_packet

    def get_rpt_packet(self):
        """
        get repeater packets
        """
        return self.rpt_packet



      # not currently used
#     def __set_rx_distance(self,distance):
#         """
#         set distance from transmitter for receiver n
#         this is a private method
#         """
#         self.__rx_distance.append(distance)

#     def set_n_beacon_packet(self,n_packet):
#         """
#         set/save nth copy of received beacon packet
#         """
#         self.n_beacon_packet.append(n_packet)
        
#     def get_rx_location_n(self,n):
#         """
#         get location of repeaters
#         if n is used, return location of receiver specified by n
#         """
#         return self.rx_location[n-1]

#     def get_rx_time_delay_n(self,n):
#         """
#         get time of arrival delay (actually time of flight) for receiver n
#         """
#         return self.rx_time_delay[n-1]

#     def get_rx_team_id_n(self,n):
#         """
#         get team id for team n
#         """
#         return self.rx_team_id[n-1]
    
#     def get_rx_power_n(self,n):
#         """
#         get rx power level at receiver n
#         """
#         return self.rx_power[n-1]

#     def __get_rx_distance(self,n):
#         """
#         set distance from transmitter for receiver n
#         this is a private method
#         """
#         return self.__rx_distance[n-1]

#     def set_simulation_area(self,bounds):
#         """
#         set bounding box on simulation's geographic coverage area
#         """
#         self.simulation_area = bounds

