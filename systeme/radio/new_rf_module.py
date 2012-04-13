#!/usr/bin/env python



import eggs as spi
import freq_utils


class RFM22(object):

    def __init__(self):
        spi.setup("/dev/spidev4.0")


    # def _set_register_0x00(self):
    #     pass

    # register 0x00 is read-only
    # register 0x01 is read-only
    # register 0x02 is read-only
    # register 0x03 is read-only
    # register 0x04 is read-only


    def _set_reg_interrupt_enable_1(self, value):
        """
        Set Interrupt Enable 1.

        This is register 0x05.
        """
        spi.write(0x05, value)


    def _set_reg_interrupt_enable_2(self, value):
        """
        Set Interrupt Enable 2.

        This is register 0x06.
        """
        spi.write(0x06, value)


    def _set_reg_operating_mode_1(self, value):
        """
        Set Operating Mode and Function Control 1.

        This is register 0x07.
        """
        spi.write(0x07, value)


    def _set_reg_operating_mode_2(self, value):
        """
        Set Operating Mode and Function Control 2.

        This is register 0x08.
        """
        spi.write(0x08, value)
        

    def _set_reg_capacitor(self, value=0x7F):
        """
        Set 30 MHz Crystal Oscillator Load Capacitance.

        This is register 0x09.
        """
        spi.write(0x09, value)


    def _set_reg_clock(self, value=0x05):
        """
        Set Microcontroller Output Clock.

        This is register 0x0A.
        """
        spi.write(0x0A, value)
        
       
    def _set_reg_GPIO_0(self, value=0xF4):
        """
        Set GPIO Configuration 0.

        This is register 0x0B.
        """
        spi.write(0x0B, value)

        
    def _set_reg_GPIO_1(self, value=0xEF):
        """
        Set GPIO Configuration 1.

        This is register 0x0C.
        """
        spi.write(0x0C, value)


    def _set_reg_GPIO_2(self, value=0x00):
        """
        Set GPIO Configuration 2.

        This is register 0x0D.
        """
        spi.write(0x0D, value)


    def _set_reg_IO_config(self, value=0x00):
        """
        Set I/O Port Configuration.

        This is register 0x0E.
        """
        spi.write(0x0E, value)


    def _set_reg_ADC_config(self, value=0x70):
        """
        Set ADC Configuration.

        This is register 0x0F.
        """
        spi.write(0x0F, 0x70)


    def _set_reg_ADC_offset(self, value=0x00):
        """
        Set ADC Sensor Amplifier Offset.

        This is register 0x10.
        """
        spi.write(0x10, value)


    # register 0x11 is read-only


    def _set_reg_temp_calibration(self, value=0x00):
        """
        Set Temperature Sensor Calibration.

        This is register 0x12.
        """
        spi.write(0x12, value)


    def _set_reg_temp_offset(self, value=0x00):
        """
        Set Temperature Value Offset.

        This is register 0x13.
        """
        spi.write(0x13, value)


    # TODO: _set_register_0x14()
    # TODO: _set_register_0x15()
    # TODO: _set_register_0x16()
    # TODO: _set_register_0x17()
    # TODO: _set_register_0x18()
    # TODO: _set_register_0x19()
    # TODO: _set_register_0x1A()
    # TODO: _set_register_0x1B()


    def _set_reg_IF_filter_bw(self, value=0x1D):
        """
        Set IF Filter Bandwith.

        This is register 0x1C.
        """
        spi.write(0x1C, value)


    def _set_reg_AFC_loop(self, value=0x40):
        """
        Set AFC Gear Loop Shift Override.

        This is register 0x1D. Note that the RFM22 referes to this
        register as ``Battery Voltage Level'', this is incorrect.
        """
        spi.write(0x1D, value)

        
    # TODO: _set_register_0x1E()


    def _set_reg_clock_recovery_gearshift_override(self, value=0x03):
        """
        Set Clock Recovery Gearshirt Override.

        This is register 0x1F.
        """
        spi.write(0x1F, value)


    def _set_reg_clock_recovery_rate(self, value=0xA1):
        """
        Set Clock Recovery Oversampling Rate.

        This is register 0x20.
        """
        spi.write(0x20, value)


    def _set_reg_clock_offset_2(self, value=0x20):
        """
        Set Clock Recovery Offset 2.

        This is register 0x21.
        """
        spi.write(0x21, value)


    def _set_reg_clock_offset_1(self, value=0x4E):
        """
        Set Clock Recovery Offset 1.

        This is register 0x22.
        """
        spi.write(0x22, value)

        
    def _set_reg_clock_offset_0(self, value=0xA5):
        """
        Set Clock Recovery Offset 0.

        This is register 0x23.
        """
        spi.write(0x23, value)


    def _set_reg_clock_gain_1(self, value=0x00):
         """
         Set Clock Recovery Timing Loop Gain 1.

         This is register 0x24.
         """
         spi.write(0x24, value)


    def _set_reg_clock_gain_0(self, value=0x0A):
         """
         Set Clock Recovery Timing Loop Gain 0.

         This is register 0x25.
         """
         spi.write(0x25, value)


    # register 0x26 is read-only

    # TODO: _set_register_0x27()
    
    # register 0x28 is read-only
    # register 0x29 is read-only
    # register 0x2A is reserved
    # register 0x2B is reserved

    def _set_reg_magic_register_0x2C(self, value=0x00):
        """
        Set magic register 0x2C. 

        No idea what this does, or if we can even do this (registers
        0x2A-0x2F are indicated as ``Reserved'' in the user manual)
        but it is in the sample program.
        """
        spi.write(0x2C, value)


    def _set_reg_magic_register_0x2D(self, value=0x00):
        """
        Set magic register 0x2D. 

        No idea what this does, or if we can even do this (registers
        0x2A-0x2F are indicated as ``Reserved'' in the user manual)
        but it is in the sample program.
        """
        spi.write(0x2D, value)


    def _set_reg_magic_register_0x2E(self, value=0x00):
        """
        Set magic register 0x2E. 

        No idea what this does, or if we can even do this (registers
        0x2A-0x2F are indicated as ``Reserved'' in the user manual)
        but it is in the sample program.
        """
        spi.write(0x2E, value)


    # register 0x2F is reserved
        

    def _set_reg_data_access_control(self, value=0x8C):
        """
        Set Data Access Control.

        This is register 0x30.
        """
        spi.write(0x30, value)


    # register 0x31 is read-only


    def _set_reg_header_control_1(self, value=0xFF):
        """
        Set Header Control 1.

        This is register 0x32.
        """
        spi.write(0x32, value)


    def _set_reg_header_control_2(self, value=0x42):
        """
        Set Header Control 2.

        This is register 0x33.
        """
        spi.write(0x33, value)


    def _set_reg_preamble_length(self, value=64):
        """
        Set Preamble Length.

        This is register 0x34.
        """
        spi.write(0x34, value)


    def _set_reg_preamble_detection(self, value=0x20):
        """
        Set Preamble Detection Control 1.

        This is register 0x35.
        """
        spi.write(0x35, value)


    def _set_reg_synch_word_3(self, value=0x2D):
        """
        Set Synchronization Word 3.

        This is register 0x36.
        """
        spi.write(0x36, value)


    def _set_reg_synch_word_2(self, value=0xD4):
        """
        Set Synchronization Word 2.

        This is register 0x37.
        """
        spi.write(0x37, value)


    def _set_reg_synch_word_1(self, value=0x00):
        """
        Set Synchronization Word 1.

        This is register 0x38.
        """
        spi.write(0x38, value)


    def _set_reg_synch_word_0(self, value=0x00):
        """
        Set Synchronization Word 0.

        This is register 0x39.
        """
        spi.write(0x39, value)


    def _set_reg_tx_header_3(self, value=0xFF):
        """
        Set Transmit Header 3.

        This is register 0x3A.
        """
        spi.write(0x3A, value)


    def _set_reg_tx_header_2(self, value=0xFF):
        """
        Set Transmit Header 2.

        This is register 0x3B.
        """
        spi.write(0x3B, value)


    def _set_reg_tx_header_1(self, value=0xFF):
        """
        Set Transmit Header 1.

        This is register 0x3C.
        """
        spi.write(0x3C, value)


    def _set_reg_tx_header_0(self, value=0xFF):
        """
        Set Transmit Header 0.

        This is register 0x3D.
        """
        spi.write(0x3D, value)


    def _set_reg_packet_length(self, value=17):
        """
        Set Packet Length.

        This is register 0x3E.
        """
        spi.write(0x3E, value)


    def _set_reg_check_header_3(self, value=0xFF):
        """
        Set Check Header 3.

        This is register 0x3F.
        """
        spi.write(0x3F, value)


    def _set_reg_check_header_2(self, value=0xFF):
        """
        Set Check Header 2.

        This is register 0x40.
        """
        spi.write(0x40, value)


    def _set_reg_check_header_1(self, value=0xFF):
        """
        Set Check Header 1.

        This is register 0x41.
        """
        spi.write(0x41, value)


    def _set_reg_check_header_0(self, value=0xFF):
        """
        Set Check Header 0.

        This is register 0x42.
        """
        spi.write(0x42, value)


    def _set_reg_header_enable_3(self, value=0xFF):
        """
        Set Header Enable 3.

        This is register 0x43.
        """
        spi.write(0x43, value)


    def _set_reg_header_enable_2(self, value=0xFF):
        """
        Set Header Enable 2.

        This is register 0x44.
        """
        spi.write(0x44, value)


    def _set_reg_header_enable_1(self, value=0xFF):
        """
        Set Header Enable 1.

        This is register 0x45.
        """
        spi.write(0x45, value)


    def _set_reg_header_enable_0(self, value=0xFF):
        """
        Set Header Enable 0.

        This is register 0x46.
        """
        spi.write(0x46, value)

        
    # register 0x47 is read-only
    # register 0x48 is read-only
    # register 0x49 is read-only
    # register 0x4A is read-only
    # register 0x4B is read-only
    # register 0x4C is reserved
    # register 0x4D is reserved
    # register 0x4E is reserved
    # register 0x4F is reserved


    # TODO: _set_register_0x50()
    # TODO: _set_register_0x52()
    # TODO: _set_register_0x53()


    # register 0x54 is reserved


    # TODO: _set_register_0x55()


    def _set_reg_modem_test(self, value=0x01):
        """
        Set Modem Test.

        This is register 0x56.
        """
        spi.write(0x56, value)


    # TODO: _set_register_0x57()


    def _set_reg_charge_pump(self, value=0x80):
        """
        Set Charge Pump Current Trimming/Override.

        This is register 0x58.
        """
        spi.write(0x58, value)

        
    def _set_reg_divider_current(self, value=0x40):
        """
        Set Divider Current Trimming/Delta-Sigma Test.

        This is register 0x59.
        """
        spi.write(0x59, value)


    def _set_reg_VCO_current(self, value=0x7F):
        """
        Set VCO Current Trimming.

        This is register 0x5A.
        """
        spi.write(0x5A, value)


    # TODO: _set_register_0x5B()
    # TODO: _set_register_0x5C()
    # TODO: _set_register_0x5D()
    # TODO: _set_register_0x58()
    # TODO: _set_register_0x5E()
    # TODO: _set_register_0x5F()

    # TODO: _set_register_0x60()
    # TODO: _set_register_0x61()
    # TODO: _set_register_0x62()
    # TODO: _set_register_0x63()
    # TODO: _set_register_0x64()
    # TODO: _set_register_0x66()
    # TODO: _set_register_0x67()


    def _set_reg_ADC_tuning_2(self, value=0x04):
        """
        Set Delta-Sigma ADC Tuning 2.

        This is register 0x68.
        """
        spi.write(0x68, value)


    # TODO: _set_register_0x69()


    def _set_reg_AGC_override_2(self, value=0x0B):
        """
        Set AGC Override 2.

        This is register 0x6A.
        """
        spi.write(0x6A, value)



    # TODO: _set_register_0x6B()
    # TODO: _set_register_0x6C()


    def _set_reg_tx_power(self, value=0x07):
        """
        Set TX Power,

        This is register 0x6D.
        """
        spi.write(0x6D, value)


    def _set_reg_tx_rate_1(self, value=0x27):
        """
        Set TX Data Rate 1.

        This is register 0x6E.
        """
        spi.write(0x6E, value)


    def _set_reg_tx_rate_0(self, value=0x52):
        """
        Set TX Data Rate 0.

        This is register 0x6F.
        """
        spi.write(0x6F, value)


    def _set_reg_modulation_mode_1(self, value=0x20):
        """
        Set Modulation Mode Control 1.

        This is register 0x70.
        """
        spi.write(0x70, value)


    def _set_reg_modulation_mode_2(self, value=0x22):
        """
        Set Modulation Mode Control 2.

        This is register 0x71.
        """
        spi.write(0x71, value)
    

    def _set_reg_freq_deviation(self, value=0x48):
        """
        Set Frequency Deviation

        This is register 0x72.
        """
        spi.write(0x72, value)


    def _set_reg_freq_offset_1(self, value=0x00):
        """
        Set Frequency Offset 1.

        This is register 0x73.
        """
        spi.write(0x73, value)


    def _set_reg_freq_offset_2(self, value=0x00):
        """
        Set Frequency Offset 2.

        This is register 0x74.
        """
        spi.write(0x74, value)
     

    def _set_reg_freq_band(self, value=0x53):
        """
        Set Frequency Band Select.

        This is register 0x75.
        """
        spi.write(0x75, value)


    def _set_reg_carrier_freq_1(self, value=0x64):
        """
        Set Nominal Carrier Frequency 1.

        This is register 0x76.
        """
        spi.write(0x76, value)


    def _set_reg_carrier_freq_0(self, value=0x00):
        """
        Set Nominal Carrier Frequency 0.

        This is register 0x77.
        """
        spi.write(0x77, value)


    # register 0x78 is reserved


    def _set_reg_freq_hopping_chan(self, value=0x00):
        """
        Set Frequency Hopping Channel Select.

        This is register 0x79.
        """
        spi.write(0x79, value)


    def _set_reg_freq_hopping_step(self, value=0x00):
        """
        Set Frequency Hopping Step Size.

        This is register 0x7A.
        """
        spi.write(0x7A, value)


    # register 0x7B is reserved


    def _set_reg_tx_fifo_control_1(self, value):
        """
        Set TX FIFO Control 1.

        This is register 0x7C.
        """
        spi.write(0x7C, value)


    def _set_reg_tx_fifo_control_2(self, value):
        """
        Set TX FIFO Control 2.

        This is register 0x7D.
        """
        spi.write(0x7D, value)


    def _set_reg_rx_fifo_control(self, value):
        """
        Set RX FIFO Control.

        This is register 0x7E.
        """
        spi.write(0x7E, value)



    # TODO: _set_register_0x7F()




    def default_rf22_setup(self):
        """
        Default setup for RFM22

        This is a default setup for the RFM 22 Radio module.
        """
        self._set_reg_capacitor()
        self._set_reg_clock()
        self._set_reg_GPIO_0()
        self._set_reg_GPIO_1()
        self._set_reg_GPIO_2()
        self._set_reg_IO_config()
        self._set_reg_ADC_config()
        self._set_reg_ADC_offset()
        self._set_reg_temp_calibration()
        self._set_reg_temp_offset()
        self._set_reg_IF_filter_bw()
        self._set_reg_AFC_loop()
        self._set_reg_clock_recovery_gearshift_override()
        self._set_reg_clock_recovery_rate()
        self._set_reg_clock_offset_2()
        self._set_reg_clock_offset_1()
        self._set_reg_clock_offset_0()
        self._set_reg_clock_gain_1()
        self._set_reg_clock_gain_0()
        self._set_reg_magic_register_0x2C()
        self._set_reg_magic_register_0x2D()
        self._set_reg_magic_register_0x2E()
        self._set_reg_data_access_control()
        self._set_reg_header_control_1()
        self._set_reg_header_control_2()
        self._set_reg_preamble_length()
        self._set_reg_preamble_detection()
        self._set_reg_synch_word_3()
        self._set_reg_synch_word_2()
        self._set_reg_synch_word_1()
        self._set_reg_synch_word_0()
        self._set_reg_tx_header_3()
        self._set_reg_tx_header_2()
        self._set_reg_tx_header_1()
        self._set_reg_tx_header_0()
        self._set_reg_packet_length()
        self._set_reg_check_header_3()
        self._set_reg_check_header_2()
        self._set_reg_check_header_1()
        self._set_reg_check_header_0()
        self._set_reg_header_enable_3()
        self._set_reg_header_enable_2()
        self._set_reg_header_enable_1()
        self._set_reg_header_enable_0()
        self._set_reg_modem_test()
        self._set_reg_charge_pump()
        self._set_reg_divider_current()
        self._set_reg_VCO_current()
        self._set_reg_ADC_tuning_2()
        self._set_reg_AGC_override_2()
        self._set_reg_tx_power()
        self._set_reg_tx_rate_1()
        self._set_reg_tx_rate_0()
        self._set_reg_modulation_mode_1()
        self._set_reg_modulation_mode_2()
        self._set_reg_freq_deviation()
        self._set_reg_freq_offset_1()
        self._set_reg_freq_offset_2()
        # self._set_reg_freq_band()
        # self._set_reg_carrier_freq_1()
        # self._set_reg_carrier_freq_0()
        self._set_reg_freq_hopping_chan()
        self._set_reg_freq_hopping_step()


    def disable_interrupts(self):
        """
        Disable all interrupts. 

        This function disables all the interrupts in register 0x05
        Interrupt Enable 1 and register 0x06 Interrupt Enable 2.
        """
        spi.write(0x05, 0x00)
        spi.write(0x06, 0x00)


    def reset_all_registers(self):
        """
        Reset all registers.

        This function resets all registers to POR state.
        """
        spi.write(0x07, 0x80)
        

    def set_frequency(self, freq):
        """
        Set the operating frequency.

        This function sets the values in registers 0x75, 0x76, 0x77,
        that determine the operating center frequency.

        Parameters
        ----------
        freq : float
            Center frequency, this should be between 240.0e6 and 930.0e6.


        Examples
        --------
        >>> set_frequency(434e6)

        """
        fc, hbsel, fb = freq_utils.carrier_freq(freq)
        freq_band = 0x40 | hbsel << 5 | fb
        self._set_reg_freq_band(freq_band)
        self._set_reg_carrier_freq_1(fc >> 8)
        self._set_reg_carrier_freq_0(fc & 0xff)




    def clear_tx_fifo(self):
        """
        Clear TX FIFO buffer.

        This function clears the TX FIFO buffer:
        - Set bit 0 (ffclrtx) in register 0x08, Operating Mode and Function Control 2.
        - Clear bit 0 (ffclrtx) in register 0x08, Operating Mode and Function Control 2.
        """
        self._set_reg_operating_mode_2(0x01)
        self._set_reg_operating_mode_2(0x00)


    def clear_rx_fifo(self):
        """
        Clear RX FIFO buffer.

        This function clears the RX FIFO buffer:
        - Set bit 1 (ffclrrx) in register 0x08, Operating Mode and Function Control 2.
        - Clear bit 1 (ffclrrx) in register 0x08, Operating Mode and Function Control 2.
        """
        self._set_reg_operating_mode_2(0x02)
        self._set_reg_operating_mode_2(0x00)


    def clear_fifo(self):
        """
        Clear TX and RX FIFO buffers.

        This function clears the TX and RX FIFO buffers:
        - Set bits 0 and 1 in register 0x08, Operating Mode and Function Control 2.
        - Clear bits 0 and 1 in register 0x08, Operating Mode and Function Control 2.
        """
        self._set_reg_operating_mode_2(0x03)
        self._set_reg_operating_mode_2(0x00)


    def load_tx_fifo(self, data):
        """
        Load TX FIFO buffer.

        This function loads data into the TX FIFO buffer.

        Parameters
        ----------
        data : array-like
            The data to load into the TX FIFO. Elements must be 8 bits,
            maximum array length is 128 elements.
        """
        for i in data:
            spi.write(0x7F, i)
        # TODO: add error/exception handling


    def set_rx_fifo_almost_full_threshold(self, threshold):
        """
        Set the RX FIFO Almost Full threshold.

        This function sets the RX Almost Full threshold. When the
        incoming RX data reaches the Almost Full Threshold an
        interrupt will be generated to the microcontroller via the
        nIRQ pin. The microcontroller will then need to read the data
        from the RX FIFO.

        Parameters
        ----------
        threshold : int
            The desired threshold value in bumber of bytes.
        """
        self._set_reg_rx_fifo_control(threshold)


    def set_tx_fifo_almost_full_threshold(self, threshold):
        """
        Set the TX FIFO Almost Full threshold.

        This function sets the TX Almost Full threshold. When the data
        being filled into the TX FIFO reaches this threshold limit, an
        interrupt to the microcontroller is generated so the module
        can enter TX mode to transmit the contents of the TX FIFO.

        Parameters
        ----------
        threshold : int
            The desired threshold value in bumber of bytes.
        """
        pass


    def set_op_mode(self, mode):
        """
        Set operating mode.

        This function sets the operating mode.

        Parameters
        ----------
        mode : str
            Operating mode, possible modes are 
            - `ready`
            - `tune`
            - `rx`
            - `tx`
        """
        if mode == 'ready':
            self._set_reg_operating_mode_1(0x01)
        elif mode == 'tune':
            self._set_reg_operating_mode_1(0x03)
        elif mode == 'rx':
            self._set_reg_operating_mode_1(0x05)
        elif mode == 'tx':
            self._set_reg_operating_mode_1(0x09)
        else:
            # TODO: add error/exception handling
            print "+++ Out of Cheese Error. Redo From Start. +++"




    def clear_interrupts(self):
        """
        Clear interrupts.

        This function clears the interrupts by reading registers 0x03
        Interrupt/Status 1 and 0x02 Interrupt Status 2.
        """
        i = spi.read(0x03)    
        i = spi.read(0x04)


    def enable_interrupt(self, signal):
        """
        Enable interrupt signals.

        This function enables interrupt signals in registers 0x05
        Interrupt Enable 1 and 0x06 Interrupt Enable 2.

        TODO: There has to be a better way to enable multiple
        interrupts then calling this function over and over.

        Parameters
        ----------
        signal : str
            Interrupt signal to be enabled. Available signals are:
            -
        """
        r1 = spi.read(0x05)
        r2 = spi.read(0x06)
        if signal == 'crc_error':
            self._set_reg_interrupt_enable_1(r1 | 0x01)
        elif signal == 'valid_packet_received':
            self._set_reg_interrupt_enable_1(r1 | 0x02)
        elif signal == 'packet_sent':
            self._set_reg_interrupt_enable_1(r1 | 0x04)
        elif signal == 'external_interrupt':
            self._set_reg_interrupt_enable_1(r1 | 0x08)
        elif signal == 'rx_fifo_almost_full':
            self._set_reg_interrupt_enable_1(r1 | 0x10)
        elif signal == 'tx_fifo_almost_empty':
            self._set_reg_interrupt_enable_1(r1 | 0x20)
        elif signal == 'tx_fifo_almost_full':
            self._set_reg_interrupt_enable_1(r1 | 0x40)
        elif signal == 'fifo_underflow_overflow':
            self._set_reg_interrupt_enable_1(r1 | 0x80)
        elif signal == 'power_on_reset':
            self._set_reg_interrupt_enable_2(r2 | 0x01)
        elif signal == 'module_ready_xtal':
            self._set_reg_interrupt_enable_2(r2 | 0x02)
        elif signal == 'low_battery_detect':
            self._set_reg_interrupt_enable_2(r2 | 0x04)
        elif signal == 'wake_up_timer':
            self._set_reg_interrupt_enable_2(r2 | 0x08)
        elif signal == 'rssi':
            self._set_reg_interrupt_enable_2(r2 | 0x10)
        elif signal == 'invalid_preamble_detected':
            self._set_reg_interrupt_enable_2(r2 | 0x20)
        elif signal == 'valid_preamble_detected':
            self._set_reg_interrupt_enable_2(r2 | 0x40)
        elif signal == 'sync_word_detected':
            self._set_reg_interrupt_enable_2(r2 | 0x80)
        else:
            # TODO: add error/exception handling
            print "+++ Melon melon melon +++"
            
