#
# AidlabNotificationHandler.py
# Aidlab-SDK
# Created by Szymon Gesicki on 09.05.2020.
#

from Aidlab.AidlabCharacteristicsUUID import AidlabCharacteristicsUUID

class AidlabNotificationHandler(object):


    def __init__(self, aidlab_address, delegate):
        self.aidlab_address = aidlab_address
        self.delegate = delegate

    def handle_notification(self, sender, data):

        try: 
            sender = sender.upper()
        except: 
            pass
        
        if sender == AidlabCharacteristicsUUID.temperatureUUID["handle"] or sender == AidlabCharacteristicsUUID.temperatureUUID["uuid"].upper():
            self.delegate.did_receive_raw_temperature(data, self.aidlab_address)

        elif sender == AidlabCharacteristicsUUID.ecgUUID["handle"] or sender == AidlabCharacteristicsUUID.ecgUUID["uuid"].upper():
            self.delegate.did_receive_raw_ecg(data, self.aidlab_address)

        elif sender == AidlabCharacteristicsUUID.batteryUUID["handle"] or sender == AidlabCharacteristicsUUID.batteryUUID["uuid"].upper():
            self.delegate.did_receive_raw_battery_level(data, self.aidlab_address)

        elif sender == AidlabCharacteristicsUUID.respirationUUID["handle"] or sender == AidlabCharacteristicsUUID.respirationUUID["uuid"].upper():
            self.delegate.did_receive_raw_respiration(data, self.aidlab_address)

        elif sender == AidlabCharacteristicsUUID.motionUUID["handle"] or sender == AidlabCharacteristicsUUID.motionUUID["uuid"].upper():
            self.delegate.did_receive_raw_imu_values(data, self.aidlab_address)

        elif sender == AidlabCharacteristicsUUID.activityUUID["handle"] or sender == AidlabCharacteristicsUUID.activityUUID["uuid"].upper():
            self.delegate.did_receive_raw_activity(data, self.aidlab_address)

        elif sender == AidlabCharacteristicsUUID.stepsUUID["handle"] or sender == AidlabCharacteristicsUUID.stepsUUID["uuid"].upper():
            self.delegate.did_receive_raw_steps(data, self.aidlab_address)

        elif sender == AidlabCharacteristicsUUID.orientationUUID["handle"] or sender == AidlabCharacteristicsUUID.orientationUUID["uuid"].upper():
            self.delegate.did_receive_raw_orientation(data, self.aidlab_address)

        elif sender == AidlabCharacteristicsUUID.heartRateUUID["handle"] or sender == AidlabCharacteristicsUUID.heartRateUUID["uuid"].upper() or sender == "2A37":
            self.delegate.did_receive_raw_heart_rate(data, self.aidlab_address)

        elif sender == AidlabCharacteristicsUUID.healthThermometerUUID["handle"] or sender == AidlabCharacteristicsUUID.healthThermometerUUID["uuid"].upper() or sender == "2A1C":
            self.delegate.did_receive_raw_health_thermometer(data, self.aidlab_address)

        elif sender == AidlabCharacteristicsUUID.soundVolumeUUID["handle"] or sender == AidlabCharacteristicsUUID.soundVolumeUUID["uuid"].upper():
            self.delegate.did_receive_raw_sound_volume(data, self.aidlab_address)

        elif sender == AidlabCharacteristicsUUID.cmdUUID["handle"] or sender == AidlabCharacteristicsUUID.cmdUUID["uuid"].upper():
            self.delegate.did_receive_raw_cmd_value(data, self.aidlab_address)

    