import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
import agent
import asyncio

# D-Bus服务配置
SERVICE_NAME = "com.redflag.AIService"
OBJECT_PATH = "/AIService"
INTERFACE_NAME = "com.redflag.AIService"

class DBusService(dbus.service.Object):
    def __init__(self):
        # 初始化总线并发布对象
        bus = dbus.SessionBus()
        bus_name = dbus.service.BusName(SERVICE_NAME, bus=bus)
        super().__init__(bus_name, OBJECT_PATH)

    @dbus.service.method(INTERFACE_NAME,
                         in_signature='s',
                         out_signature='b')
    def call(self, funcName):
        print(f"Calling function: {funcName}")
        asyncio.run(agent.run_agent(funcName, self))
        return True

    @dbus.service.method(INTERFACE_NAME,
                         in_signature='s',
                         out_signature='b')
    def insert_embedding_data(self, filepath):
        print(f"Inserting filepath: {filepath}")
        return True

    @dbus.service.method(INTERFACE_NAME,
                    in_signature='s',
                    out_signature='b')
    def insert_web_addr(self, webpaths):
        print(f"Inserting webpaths: {webpaths}")
        return True

    @dbus.service.signal(INTERFACE_NAME, signature='s')
    def message_response(self, response):
        return response

if __name__ == "__main__":
    # 初始化主循环 
    DBusGMainLoop(set_as_default=True)
    loop = GLib.MainLoop()
    
    # 创建服务实例
    service = DBusService()
    print(f"D-Bus service '{SERVICE_NAME}' running...")
    
    try:
        loop.run()
    except KeyboardInterrupt:
        print("Service stopped")
        loop.quit()