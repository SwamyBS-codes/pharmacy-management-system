import React, { useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Environment, MeshTransmissionMaterial } from '@react-three/drei';
import * as THREE from 'three';

type Pill = {
  position: [number, number, number];
  rotation: [number, number, number];
  type: 'capsule' | 'tablet';
  color: string;
  floatSpeed: number;
};

function FloatingPills() {
  const pills = useMemo<Pill[]>(() => {
    const colors = ['#7dd3fc', '#a78bfa', '#34d399', '#f59e0b'];
    const arr: Pill[] = [];
    for (let i = 0; i < 18; i++) {
      const type = i % 3 === 0 ? 'tablet' : 'capsule';
      arr.push({
        position: [
          (Math.random() - 0.5) * 8,
          (Math.random() - 0.5) * 4,
          -2 - Math.random() * 2,
        ],
        rotation: [
          Math.random() * Math.PI,
          Math.random() * Math.PI,
          Math.random() * Math.PI,
        ],
        type,
        color: colors[i % colors.length],
        floatSpeed: 0.25 + Math.random() * 0.6,
      });
    }
    return arr;
  }, []);

  useFrame(({ clock, scene }) => {
    const t = clock.getElapsedTime();
    scene.traverse((obj) => {
      if (obj.userData && obj.userData.floatIndex !== undefined) {
        const i = obj.userData.floatIndex as number;
        const speed = obj.userData.floatSpeed as number;
        const baseY = obj.userData.baseY as number;
        obj.position.y = baseY + Math.sin(t * speed + i) * 0.15;
        obj.rotation.y += 0.0015;
        obj.rotation.x += 0.0007;
      }
    });
  });

  return (
    <group>
      {pills.map((pill, i) => (
        <group
          key={i}
          position={pill.position}
          rotation={pill.rotation}
          userData={{ floatIndex: i, floatSpeed: pill.floatSpeed, baseY: pill.position[1] }}
        >
          {pill.type === 'capsule' ? (
            <mesh>
              {/* Capsule */}
              <capsuleGeometry args={[0.28, 0.9, 10, 20]} />
              <MeshTransmissionMaterial
                samples={8}
                thickness={0.4}
                roughness={0.18}
                transmission={1}
                ior={1.25}
                chromaticAberration={0.02}
                anisotropy={0.15}
                distortion={0.06}
                temporalDistortion={0.12}
                attenuationDistance={0.8}
                attenuationColor={pill.color}
                background={new THREE.Color('#ffffff')}
              />
            </mesh>
          ) : (
            <mesh rotation={[Math.PI / 2, 0, 0]}>
              {/* Tablet (flat cylinder) */}
              <cylinderGeometry args={[0.38, 0.38, 0.12, 32]} />
              <MeshTransmissionMaterial
                samples={8}
                thickness={0.35}
                roughness={0.2}
                transmission={1}
                ior={1.22}
                chromaticAberration={0.015}
                anisotropy={0.1}
                distortion={0.05}
                temporalDistortion={0.1}
                attenuationDistance={0.9}
                attenuationColor={pill.color}
                background={new THREE.Color('#ffffff')}
              />
            </mesh>
          )}
        </group>
      ))}
    </group>
  );
}

export default function BackgroundPharmaScene({ className }: { className?: string }) {
  return (
    <div className={className} style={{ pointerEvents: 'none' }}>
      <Canvas
        dpr={[1, 1.5]}
        gl={{ powerPreference: 'high-performance', antialias: false }}
        camera={{ position: [0, 0, 6], fov: 55 }}
      >
        <ambientLight intensity={0.2} />
        <directionalLight position={[3, 2, 5]} intensity={0.7} />
        <Environment preset="sunset" />
        <FloatingPills />
      </Canvas>
      {/* Soft gradient overlay to keep background subtle */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background:
            'radial-gradient(60% 50% at 50% 0%, rgba(16, 185, 129, 0.06) 0%, rgba(99, 102, 241, 0.04) 50%, rgba(255, 255, 255, 0) 100%)',
        }}
      />
    </div>
  );
}
