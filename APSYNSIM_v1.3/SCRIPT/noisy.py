
def heghelp_gridUV(self, antidx=-1):

    totsampling = np.zeros((self.Npix,self.Npix),dtype=np.float32)
    Gsampling = np.zeros((self.Npix,self.Npix),dtype=np.complex64)
    Grobustsamp = np.zeros((self.Npix,self.Npix),dtype=np.complex64)
    u = np.zeros((NBmax,self.nH))
    v = np.zeros((NBmax,self.nH))
    Np4 = self.Npix/4
    
    accum = np.zeros((self.Npix,self.Npix),dtype=np.complex64)

   #slice it up so these are sampled from current noisy model part 
    step=1
    for i in range(0, self.nH, step):
        u[:,i:i+step] = self.u[:,i:i+step]
        v[:,i:i+step] = self.v[:,i:i+step]

        if antidx==-1:
            bas2change = range(self.Nbas)
            pixpos = [[] for nb in bas2change]
            totsampling[:] = 0.0
            Gsampling[:] = 0.0
        elif antidx < self.Nant:
            bas2change = map(int,list(self.basnum[antidx].flatten()))
        else:
            bas2change = []

        self.UVpixsize = 2./(self.imsize*np.pi/180./3600.)

        for nb in bas2change:
            pixU = np.rint(u[nb]/self.UVpixsize).flatten().astype(np.int32)
            pixV = np.rint(v[nb]/self.UVpixsize).flatten().astype(np.int32)
            goodpix = np.logical_and(np.abs(pixU)<self.Nphf,np.abs(pixV)<self.Nphf)
            pU = pixU[goodpix] + self.Nphf
            pV = pixV[goodpix] + self.Nphf
            mU = -pixU[goodpix] + self.Nphf
            mV = -pixV[goodpix] + self.Nphf

            pixpos[nb] = [np.copy(pU),np.copy(pV),np.copy(mU),np.copy(mV)]
            totsampling[pV,mU] += 1.0
            totsampling[mV,pU] += 1.0
            Gsampling[pV,mU] += self.Gains[nb,goodpix]
            Gsampling[mV,pU] += np.conjugate(self.Gains[nb,goodpix])

        #Changed self.nH to 5 in this 
        robfac = (5.*10.**(-self.robust))**2.*(2.*self.Nbas*step)/np.sum(self.totsampling**2.)  
          
          
          
        #Get beam scale and robust shit
        Grobustsamp[:] = Gsampling/(1.+robfac*totsampling)


        ###Hegedus adding gaussian random noise 
        modelimNoise = self.modelimTrue + np.random.normal(0, np.amax(self.modelimTrue)*.01, np.shape(self.modelimTrue))
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
        
        accum += noisemodelfft*np.fft.ifftshift(Grobustsamp)
        
        

    self.dirtymap[:] = (np.fft.fftshift(np.fft.ifft2(accum))).real/(1.+self.W2W1)
 
    self.dirtymap /= beamScale

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


