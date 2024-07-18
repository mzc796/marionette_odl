from mininet.topo import Topo
"""Custom topology example

This is the Figure 7 Fat Tree Topology in the paper

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

class MyTopo( Topo ):

	def build( self ):

		Switch1 = self.addSwitch('s1')
		Switch2 = self.addSwitch('s2')
		Switch3 = self.addSwitch('s3')
		Switch4 = self.addSwitch('s4')
		Switch5 = self.addSwitch('s5')
		Switch6 = self.addSwitch('s6')
		Switch7 = self.addSwitch('s7')
		Switch8 = self.addSwitch('s8')
		Switch9 = self.addSwitch('s9')
		Switch10 = self.addSwitch('s10')
		Switch11 = self.addSwitch('s11')
		Switch12 = self.addSwitch('s12')
		Switch13 = self.addSwitch('s13')
		Switch14 = self.addSwitch('s14')
		Switch15 = self.addSwitch('s15')
		Switch16 = self.addSwitch('s16')
		Switch17 = self.addSwitch('s17')
		Switch18 = self.addSwitch('s18')
		Switch19 = self.addSwitch('s19')
		Switch20 = self.addSwitch('s20')
		Switch21 = self.addSwitch('s21')
		Switch22 = self.addSwitch('s22')
		Switch23 = self.addSwitch('s23')
		Switch24 = self.addSwitch('s24')
		Switch25 = self.addSwitch('s25')
		Switch26 = self.addSwitch('s26')
		Switch27 = self.addSwitch('s27')
		Switch28 = self.addSwitch('s28')
		Switch29 = self.addSwitch('s29')
		Switch30 = self.addSwitch('s30')
		Switch31 = self.addSwitch('s31')
		Switch32 = self.addSwitch('s32')
		Switch33 = self.addSwitch('s33')
		Switch34 = self.addSwitch('s34')
		Switch35 = self.addSwitch('s35')
		Switch36 = self.addSwitch('s36')


		self.addLink(Switch1,Switch5)
		self.addLink(Switch1,Switch7)
		self.addLink(Switch1,Switch9)
		self.addLink(Switch1,Switch11)
		
		self.addLink(Switch2,Switch5)
		self.addLink(Switch2,Switch7)
		self.addLink(Switch2,Switch9)
		self.addLink(Switch2,Switch11)
		
		self.addLink(Switch3,Switch6)
		self.addLink(Switch3,Switch8)
		self.addLink(Switch3,Switch10)
		self.addLink(Switch3,Switch12)
		
		self.addLink(Switch4,Switch6)
		self.addLink(Switch4,Switch8)
		self.addLink(Switch4,Switch10)
		self.addLink(Switch4,Switch12)
		
		self.addLink(Switch5,Switch13)
		self.addLink(Switch5,Switch14)
		
		self.addLink(Switch6,Switch13)
		self.addLink(Switch6,Switch14)
		
		self.addLink(Switch7,Switch15)
		self.addLink(Switch7,Switch16)
		
		self.addLink(Switch8,Switch15)
		self.addLink(Switch8,Switch16)
		
		self.addLink(Switch9,Switch17)
		self.addLink(Switch9,Switch18)
		
		self.addLink(Switch10,Switch17)
		self.addLink(Switch10,Switch18)
		
		self.addLink(Switch11,Switch19)
		self.addLink(Switch11,Switch20)
		
		self.addLink(Switch12,Switch19)
		self.addLink(Switch12,Switch20)
		
		self.addLink(Switch13,Switch21)
		self.addLink(Switch13,Switch22)
		
		self.addLink(Switch14,Switch23)
		self.addLink(Switch14,Switch24)
		
		self.addLink(Switch15,Switch25)
		self.addLink(Switch15,Switch26)
		
		self.addLink(Switch16,Switch27)
		self.addLink(Switch16,Switch28)
		
		self.addLink(Switch17,Switch29)
		self.addLink(Switch17,Switch30)
		
		self.addLink(Switch18,Switch31)
		self.addLink(Switch18,Switch32)
		
		self.addLink(Switch19,Switch33)
		self.addLink(Switch19,Switch34)
		
		self.addLink(Switch20,Switch35)
		self.addLink(Switch20,Switch36)
		
		Host1 = self.addHost('h1', ip = '10.0.0.1/24')
		self.addLink(Host1,Switch21)
		Host2 = self.addHost('h2', ip = '10.0.0.2/24')
		self.addLink(Host2,Switch22)
		Host3 = self.addHost('h3', ip = '10.0.0.3/24')
		self.addLink(Host3,Switch23)
		Host4 = self.addHost('h4', ip = '10.0.0.4/24')
		self.addLink(Host4,Switch24)
		Host5 = self.addHost('h5', ip = '10.0.0.5/24')
		self.addLink(Host5,Switch25)
		Host6 = self.addHost('h6', ip = '10.0.0.6/24')
		self.addLink(Host6,Switch26)
		Host7 = self.addHost('h7', ip = '10.0.0.7/24')
		self.addLink(Host7,Switch27)
		Host8 = self.addHost('h8', ip = '10.0.0.8/24')
		self.addLink(Host8,Switch28)
		Host9 = self.addHost('h9', ip = '10.0.0.9/24')
		self.addLink(Host9,Switch29)
		Host10 = self.addHost('h10', ip = '10.0.0.10/24')
		self.addLink(Host10,Switch30)
		Host11 = self.addHost('h11', ip = '10.0.0.11/24')
		self.addLink(Host11,Switch31)
		Host12 = self.addHost('h12', ip = '10.0.0.12/24')
		self.addLink(Host5,Switch32)
		Host13 = self.addHost('h13', ip = '10.0.0.13/24')
		self.addLink(Host6,Switch33)
		Host14 = self.addHost('h14', ip = '10.0.0.14/24')
		self.addLink(Host7,Switch34)
		Host15 = self.addHost('h15', ip = '10.0.0.15/24')
		self.addLink(Host8,Switch35)
		Host16 = self.addHost('h16', ip = '10.0.0.16/24')
		self.addLink(Host9,Switch36)

topos = { 'mytopo': (lambda: MyTopo() ) }
