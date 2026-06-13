import { Canvas } from '@react-three/fiber';
import { OrbitControls, Environment, MeshTransmissionMaterial } from '@react-three/drei';
import React, { useRef } from 'react';
import * as THREE from 'three';

function BrainShape() {
  const group = useRef<THREE.Group>(null);

  // Animate slow rotation
  React.useEffect(() => {
    let frameId: number;
    const animate = () => {
      if (group.current) {
        group.current.rotation.y += 0.002;
        group.current.rotation.x += 0.001;
      }
      frameId = requestAnimationFrame(animate);
    };
    frameId = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(frameId);
  }, []);

  // Use multiple torus knots to mimic complex "brain-like" folds
  return (
    <group ref={group}>
      <mesh scale={[1.1, 1.0, 1.1]}> 
        <torusKnotGeometry args={[1.1, 0.22, 220, 32, 2, 3]} />
        <MeshTransmissionMaterial
          samples={8}
          thickness={0.45}
          roughness={0.12}
          transmission={1}
          ior={1.2}
          chromaticAberration={0.015}
          anisotropy={0.2}
          distortion={0.1}
          temporalDistortion={0.2}
          attenuationDistance={0.6}
          attenuationColor="#7dd3fc"
          background={new THREE.Color('#ffffff')}
        />
      </mesh>
      <mesh scale={[0.8, 0.8, 0.8]} rotation={[0, Math.PI / 3, 0]}> 
        <torusKnotGeometry args={[1.1, 0.18, 200, 24, 3, 7]} />
        <MeshTransmissionMaterial
          samples={8}
          thickness={0.35}
          roughness={0.15}
          transmission={1}
          ior={1.25}
          chromaticAberration={0.02}
          anisotropy={0.15}
          distortion={0.12}
          temporalDistortion={0.18}
          attenuationDistance={0.7}
          attenuationColor="#a78bfa"
          background={new THREE.Color('#ffffff')}
        />
      </mesh>
    </group>
  );
}

export default function GlassBrain({ className }: { className?: string }) {
  return (
    <div className={className}>
      <Canvas camera={{ position: [0, 0, 4], fov: 45 }}>
        {/* Lighting & environment for glassy look */}
        <ambientLight intensity={0.1} />
        <directionalLight position={[3, 3, 5]} intensity={0.8} />
        <Environment preset="city" />

        {/* The brainy shape */}
        <BrainShape />

        {/* Gentle controls */}
        <OrbitControls enablePan={false} enableZoom={false} autoRotate autoRotateSpeed={0.6} />
      </Canvas>
    </div>
  );
}
