import { Pressable, StyleSheet, View } from 'react-native';

import { ClayGloss } from '@/components/ClayGloss';
import { GradFill } from '@/components/GradFill';
import { Icon, type IconName } from '@/components/Icon';
import { Txt } from '@/components/Txt';
import { clay, color, gradient, icon, radius, rhythm, size } from '@/theme/tokens';

/**
 * §7.7 — yüzen sekme çubuğu + merkez eylem.
 * Faz 1: 3 sekme + FAB. Etiketsiz ikon YOK.
 * FAB bar üst kenarından 16 yukarı taşar, sağdan 8.
 */
export type TabKey = 'gunluk' | 'tasarruflar' | 'profil';

const SEKMELER: { key: TabKey; ad: string; ikon: IconName }[] = [
  { key: 'gunluk', ad: 'Günlük', ikon: 'gauge' },
  { key: 'tasarruflar', ad: 'Tasarruf', ikon: 'notebook' },
  { key: 'profil', ad: 'Profil', ikon: 'user' },
];

export function TabBar({
  active,
  onSelect,
  onAdd,
  fabGoster = true,
}: {
  active: TabKey;
  onSelect?: (key: TabKey) => void;
  onAdd?: () => void;
  /**
   * v4 E-10 — "bugün boş" CTA'sı zaten aynı eylemi sunarken FAB gizlenir
   * (ekranın tek birincil eylemi kalsın, §7.1). Diğer tüm ekranlarda görünür.
   */
  fabGoster?: boolean;
}) {
  return (
    <View style={stil.alan}>
      <View style={stil.cubuk}>
        <ClayGloss />
        {SEKMELER.map((s) => {
          const aktif = s.key === active;
          const tone = aktif ? color.primaryText : color.text2;
          return (
            <Pressable
              key={s.key}
              onPress={() => onSelect?.(s.key)}
              accessibilityRole="tab"
              accessibilityLabel={`${s.ad} sekmesi`}
              accessibilityState={{ selected: aktif }}
              style={stil.sekme}>
              <View
                style={[
                  stil.ikonKab,
                  aktif && {
                    height: size.tabIconBoxHeightActive,
                    backgroundColor: color.primarySoft,
                    boxShadow: clay.sunken,
                  },
                ]}>
                <Icon name={s.ikon} size={size.icon} color={tone} />
              </View>
              <View style={{ height: rhythm.sameObject }} />
              <Txt
                role={aktif ? 'label' : 'caption'}
                tone={tone}
                numberOfLines={1}
                style={stil.sekmeEtiketi}>
                {s.ad}
              </Txt>
            </Pressable>
          );
        })}
        {/* FAB'ın yerini açan boşluk — sekmeler ortalanmış kalsın */}
        <View style={stil.bosluk} />
      </View>

      {fabGoster ? <FloatingAdd onPress={onAdd} /> : null}
    </View>
  );
}

function FloatingAdd({ onPress }: { onPress?: () => void }) {
  return (
    <Pressable
      onPress={onPress}
      accessibilityRole="button"
      accessibilityLabel="Harcama ekle"
      style={({ pressed }) => [
        stil.fab,
        {
          backgroundColor: pressed ? color.primaryPress : color.primaryDeep,
          boxShadow: pressed ? clay.actionPressed : clay.action,
        },
      ]}>
      {({ pressed }) => (
        <>
          <GradFill colors={pressed ? gradient.actionPressed : gradient.action} />
          <Icon
            name="plus"
            size={size.iconFab}
            color={color.onPrimary}
            strokeWidth={icon.strokeWidthFab}
          />
        </>
      )}
    </Pressable>
  );
}

const stil = StyleSheet.create({
  alan: { height: size.tabAreaHeight },
  cubuk: {
    position: 'absolute',
    left: 0,
    right: 0,
    bottom: 0,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    height: size.tabBarHeight,
    paddingHorizontal: size.tabBarPadX,
    borderRadius: radius.pill,
    backgroundColor: color.surface,
    boxShadow: clay.raisedLg,
    overflow: 'hidden',
  },
  sekme: {
    flex: 1,
    minWidth: 0,
    height: size.tabItemHeight,
    alignItems: 'center',
    justifyContent: 'center',
  },
  ikonKab: {
    width: size.tabIconBox,
    height: size.tabIconBoxHeight,
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: radius.pill,
  },
  sekmeEtiketi: { width: '100%', textAlign: 'center' },
  bosluk: { width: size.tabItemWidth, height: size.tabItemHeight },
  fab: {
    position: 'absolute',
    right: size.fabRight,
    top: 0,
    width: size.fab,
    height: size.fab,
    borderRadius: radius.pill,
    alignItems: 'center',
    justifyContent: 'center',
    overflow: 'hidden',
  },
});
