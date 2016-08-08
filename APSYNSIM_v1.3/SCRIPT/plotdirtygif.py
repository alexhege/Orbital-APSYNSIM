
  def _plotDirty(self,redo=True, gifStep = -1, stepSize = 1):
  
    
    Np4 = self.Npix/4
    ##Do noisy to add different noise every step steps and sample fourier plane from that
    thermalNoise = False
    customNoise = True
    customRMS = .0000000001
    
    gifMode = False
    
  
    if gifStep == 0:
      #self.accumGsampling = np.zeros((self.Npix,self.Npix),dtype=np.complex64)
      
      self.accum = np.zeros((self.Npix,self.Npix),dtype=np.complex64)
      
    
    if gifStep != -1:
    
      Gsampling = np.zeros((self.Npix,self.Npix),dtype=np.complex64)
      
      for nb in range(self.nBas):
        pixU = np.rint(self.u[nb, gifStep:gifStep+stepSize]/self.UVpixsize).flatten().astype(np.int32)
        pixV = np.rint(self.v[nb, gifStep:gifStep+stepSize]/self.UVpixsize).flatten().astype(np.int32)
        goodpix = np.logical_and(np.abs(pixU)<self.Nphf,np.abs(pixV)<self.Nphf)
        pU = pixU[goodpix] + self.Nphf
        pV = pixV[goodpix] + self.Nphf
        mU = -pixU[goodpix] + self.Nphf
        mV = -pixV[goodpix] + self.Nphf

        pixpos[nb] = [np.copy(pU),np.copy(pV),np.copy(mU),np.copy(mV)]
        totsampling[pV,mU] += 1.0
        totsampling[mV,pU] += 1.0
        gpix = np.zeros((self.nH), dtype=bool)
        gpix[gifStep:gifStep+stepSize]= goodpix
        Gsampling[pV,mU] += self.Gains[nb,gpix]
        Gsampling[mV,pU] += np.conjugate(self.Gains[nb,gpix])

      
      ###Hegedus adding gaussian random noise
      
      if thermalNoise:
      
        mhz = 3.e2/(self.wavelength*1000.)

        Tgal = 9.e7*mhz**(-2.477) # approx expression for Tgal from Cane 1970 plot #15000000. #For 1 MHz
        print 'Using tgal of ' + str(Tgal)
        solidAngleAntenna = 3. #in steradians, 3 taken from LWA antenna
        #better Ae calculation from lwa paper
        Ae = .8* (self.Nant*(self.wavelength*1000.)**2/solidAngleAntenna)*np.sqrt(self.Nant*(self.Nant - 1))
        #Ae = .8*((800000./2.)**2*np.pi)
        k = 1.38e-23
        sefd = 2*k*Tgal/Ae*10**26
        bandwidth = 32000
        intTime = .1 #seconds
        Srms =  sefd/(np.sqrt(intTime*bandwidth))
        if customNoise:
          Srms = customRMS

        print 'Using noise of ' + str(Srms)

        modelimNoise = self.modelimTrue + np.random.normal(0, Srms, np.shape(self.modelimTrue))
        modelimNoise[modelimNoise<0.0] = 0.0

        if self.Diameters[0]>0.0:
          PB = 2.*(1220.*180./np.pi*3600.*self.wavelength/self.Diameters[0]/2.3548)**2.  # 2*sigma^2 #Strehl Ratio???
          #  print PB, np.max(self.distmat),self.wavelength
          beamImg = np.exp(self.distmat/PB)
          modelim = modelimNoise*beamImg 
        else:
          modelim = modelimNoise

        modelfft = np.fft.fft2(np.fft.fftshift(modelim))
        
        
      else:
        modelfft = self.modelfft

          
      self.accum += modelfft*np.fft.ifftshift(Gsampling)
      
      
      accum = self.accum/(1.+self.robfac*self.totsampling)  
      
      self.dirtymap[:] = (np.fft.fftshift(np.fft.ifft2(accum))).real/(1.+self.W2W1)
   
      self.dirtymap /= self.beamScale
        
    #not in gifmode, gifstep == -1  
    else:
      
      if thermalNoise:
      
        dirtymap = np.zeros((self.Npix,self.Npix),dtype=np.float32)
      
        mhz = 3.e2/(self.wavelength*1000.)

        Tgal = 9.e7*mhz**(-2.477) # approx expression for Tgal from Cane 1970 plot #15000000. #For 1 MHz
        print 'Using tgal of ' + str(Tgal)
        solidAngleAntenna = 3. #in steradians, 3 taken from LWA antenna
        #better Ae calculation from lwa paper
        Ae = .8* (self.Nant*(self.wavelength*1000.)**2/solidAngleAntenna)*np.sqrt(self.Nant*(self.Nant - 1))
        #Ae = .8*((800000./2.)**2*np.pi)
        k = 1.38e-23
        sefd = 2*k*Tgal/Ae*10**26
        bandwidth = 32000
        intTime = .1 #seconds
        Srms =  sefd/(np.sqrt(intTime*bandwidth))
        if customNoise:
          Srms = customRMS

        print 'Using noise of ' + str(Srms)
              
        totsampling = np.zeros((self.Npix,self.Npix),dtype=np.float32)
        Gsampling = np.zeros((self.Npix,self.Npix),dtype=np.complex64)
        Grobustsamp = np.zeros((self.Npix,self.Npix),dtype=np.complex64)
        u = np.zeros((self.Nbas,self.nH))
        v = np.zeros((self.Nbas,self.nH))
        
        
        accumGsampling = np.zeros((self.Npix,self.Npix),dtype=np.complex64)
        
        accum = np.zeros((self.Npix,self.Npix),dtype=np.complex64)

       #slice it up so these are sampled from current noisy model part 
        for i in range(0, self.nH, stepSize):
       
          pixpos = [[] for nb in range(self.Nbas)]
          #totsampling[:] = 0.0
          Gsampling[:] = 0.0


          self.UVpixsize = 2./(self.imsize*np.pi/180./3600.)

          for nb in range(self.Nbas):
            pixU = np.rint(self.u[nb, i:i+stepSize]/self.UVpixsize).flatten().astype(np.int32)
            pixV = np.rint(self.v[nb, i:i+stepSize]/self.UVpixsize).flatten().astype(np.int32)
            goodpix = np.logical_and(np.abs(pixU)<self.Nphf,np.abs(pixV)<self.Nphf)
            pU = pixU[goodpix] + self.Nphf
            pV = pixV[goodpix] + self.Nphf
            mU = -pixU[goodpix] + self.Nphf
            mV = -pixV[goodpix] + self.Nphf

            pixpos[nb] = [np.copy(pU),np.copy(pV),np.copy(mU),np.copy(mV)]
            totsampling[pV,mU] += 1.0
            totsampling[mV,pU] += 1.0
            gpix = np.zeros((self.nH), dtype=bool)
            gpix[i:i+stepSize] = goodpix
            Gsampling[pV,mU] += self.Gains[nb,gpix]
            Gsampling[mV,pU] += np.conjugate(self.Gains[nb,gpix])
           

          ###Hegedus adding gaussian random noise

          modelimNoise = self.modelimTrue + np.random.normal(0, Srms, np.shape(self.modelimTrue))
          modelimNoise[modelimNoise<0.0] = 0.0

          if self.Diameters[0]>0.0:
            PB = 2.*(1220.*180./np.pi*3600.*self.wavelength/self.Diameters[0]/2.3548)**2.  # 2*sigma^2 #Strehl Ratio???
            #  print PB, np.max(self.distmat),self.wavelength
            beamImg = np.exp(self.distmat/PB)
            modelim = modelimNoise*beamImg 
          else:
            modelim = modelimNoise

          noisemodelfft = np.fft.fft2(np.fft.fftshift(modelim))

          ###Done edit
            
          accum += noisemodelfft*np.fft.ifftshift(Gsampling)
         
            
        #for swtch from grobustsamp to gsampling above for gif ease    
        accum = accum/(1.+self.robfac*self.totsampling)  

        self.dirtymap[:] = (np.fft.fftshift(np.fft.ifft2(accum))).real/(1.+self.W2W1)
     
        self.dirtymap /= self.beamScale
    ####DONE NOISY

      else:

        self.dirtymap[:] = (np.fft.fftshift(np.fft.ifft2(self.modelfft*np.fft.ifftshift(self.Grobustsamp)))).real/(1.+self.W2W1)

        if self.Nant2 > 1:
          self.dirtymap[:] += (np.fft.fftshift(np.fft.ifft2(self.modelfft2*np.fft.ifftshift(self.robustsamp2)))).real*(self.W2W1/(1.+self.W2W1))
          self.dirtymap /= self.beamScale2
        else:
          self.dirtymap /= self.beamScale


    extr = [np.min(self.dirtymap),np.max(self.dirtymap)]
    if redo:
      self.dirtyPlot.cla()
      self.dirtyPlotPlot = self.dirtyPlot.imshow(self.dirtymap[Np4:self.Npix-Np4,Np4:self.Npix-Np4],interpolation='nearest',picker=True, cmap=self.currcmap)
      modflux = self.dirtymap[self.Nphf,self.Nphf]
      self.dirtyText = self.dirtyPlot.text(0.05,0.87,self.fmtD%(modflux,0.0,0.0),
         transform=self.dirtyPlot.transAxes,bbox=dict(facecolor='white', 
         alpha=0.7))
      pl.setp(self.dirtyPlotPlot, extent=(self.Xaxmax/2.,-self.Xaxmax/2.,-self.Xaxmax/2.,self.Xaxmax/2.))
      self.curzoom[1] = (self.Xaxmax/2.,-self.Xaxmax/2.,-self.Xaxmax/2.,self.Xaxmax/2.)
      self.dirtyPlot.set_ylabel('Dec offset (as)')
      self.dirtyPlot.set_xlabel('RA offset (as)')
      self.dirtyPlot.set_title('DIRTY IMAGE')
    else:
      self.dirtyPlotPlot.set_data(self.dirtymap[Np4:self.Npix-Np4,Np4:self.Npix-Np4])
      self.dirtyPlotPlot.norm.vmin = extr[0]
      self.dirtyPlotPlot.norm.vmax = extr[1]





